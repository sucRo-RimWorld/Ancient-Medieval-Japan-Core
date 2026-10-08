# Shared by staging, config generation, runtime runner and tooling regression.
function Get-GrainsTestProfile([string]$Name) {
    if ($Name -notin @('vanilla', 'vanilla-ccto', 'mo', 'mo-ccto')) {
        throw "Unknown Grains test profile: $Name"
    }
    $useMO = $Name -in @('mo', 'mo-ccto')
    $useCCTO = $Name -in @('vanilla-ccto', 'mo-ccto')
    $providers = @()
    if ($useMO) { $providers += 'dankpyon.medieval.overhaul' }
    if ($useCCTO) { $providers += 'sucro.cropcoldtoleranceoverhaul' }
    [pscustomobject]@{
        Name = $Name
        UseMO = $useMO
        UseCCTO = $useCCTO
        Providers = $providers
        Feature = "grains-$Name.feature"
        Scenarios = @(
            "Grains $Name loads the requested real providers",
            "Grains $Name primary grain loop resolves",
            "Grains $Name optional cold tolerance resolves",
            "Grains $Name wheat flour and minimum food resolve",
            "Grains $Name seven grains retain environmental niches",
            "Grains $Name real harvest and flour food Bills complete"
        )
    }
}

# Resolve only declared hard dependencies, then order active loadAfter edges.
# Never reuse the player's active mod list or activate all installed mods.
function Get-GrainsActiveMods([object]$Profile, [hashtable]$Installed) {
    $ordered = New-Object 'System.Collections.Generic.List[string]'
    $visiting = @{}
    $visited = @{}
    function Visit([string]$Id) {
        $Id = $Id.ToLowerInvariant()
        if ($visited.ContainsKey($Id)) { return }
        if ($visiting.ContainsKey($Id)) { throw "Mod dependency cycle at $Id" }
        if (-not $Installed.ContainsKey($Id)) { throw "Required installed mod missing: $Id" }
        if ($Id -like 'sucro.ancientmedievaljapan.core.*fixture' -or $Id -eq 'sucro.ancientmedievaljapan.core') {
            throw "Production Core or API fixture cannot participate in a Grains profile: $Id"
        }
        if ((-not $Profile.UseMO -and $Id -eq 'dankpyon.medieval.overhaul') -or
            (-not $Profile.UseCCTO -and $Id -eq 'sucro.cropcoldtoleranceoverhaul')) {
            throw "Profile $($Profile.Name) forbids dependency $Id"
        }
        $visiting[$Id] = $true
        foreach ($dependency in @($Installed[$Id].Xml.ModMetaData.modDependencies.li)) {
            $depId = ([string]$dependency.packageId).Trim()
            if ($depId) { Visit $depId }
        }
        $visiting.Remove($Id)
        $visited[$Id] = $true
        $ordered.Add($Id)
    }
    foreach ($id in @('brrainz.harmony', 'ludeon.rimworld') + @($Profile.Providers) + @(
        'sucro.ancientmedievaljapan.core.e2etarget', 'rimworks.rimlogging',
        'rimworks.pickle', 'rimworks.quickstarts', 'sucro.ancientmedievaljapan.core.e2e')) { Visit $id }

    $result = New-Object 'System.Collections.Generic.List[string]'
    $pending = @($ordered)
    while ($pending.Count -gt 0) {
        $ready = @($pending | Where-Object {
            $id = $_
            $before = @($Installed[$id].Xml.ModMetaData.modDependencies.li | ForEach-Object { [string]$_.packageId }) +
                @($Installed[$id].Xml.ModMetaData.loadAfter.li) + @($Installed[$id].Xml.ModMetaData.forceLoadAfter.li)
            @($before | Where-Object { $_ -and $pending -contains ([string]$_).ToLowerInvariant() }).Count -eq 0
        })
        if ($ready.Count -eq 0) { throw "Active load-order cycle: $($pending -join ', ')" }
        foreach ($id in $ready) { $result.Add($id) }
        $pending = @($pending | Where-Object { $ready -notcontains $_ })
    }
    return $result.ToArray()
}
