$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
public static class GrainOutlinePalette {
 public static int Export(string source, string target) {
  using (var src = new Bitmap(source))
  using (var dst = new Bitmap(src.Width,src.Height,PixelFormat.Format32bppArgb)) {
   int changed=0;
   for(int y=0;y<src.Height;y++) for(int x=0;x<src.Width;x++) {
    Color c=src.GetPixel(x,y);
    int max=Math.Max(c.R,Math.Max(c.G,c.B));
    int min=Math.Min(c.R,Math.Min(c.G,c.B));
    if(c.A>0 && max<115 && max-min<30) {
     c=Color.FromArgb(c.A,77,78,60); changed++;
    }
    dst.SetPixel(x,y,c);
   }
   dst.Save(target,ImageFormat.Png);
   return changed;
  }
 }
}
'@
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'generation.json') -Raw | ConvertFrom-Json
$sourceDir = Join-Path $PSScriptRoot 'Sources'
$normalizedDir = Join-Path $PSScriptRoot 'Normalized'
New-Item -ItemType Directory -Path $sourceDir,$normalizedDir -Force | Out-Null
foreach ($asset in $manifest.assets.PSObject.Properties) {
 $original = $asset.Value.path
 $source = Join-Path $sourceDir ($asset.Name + '.png')
 if (Test-Path -LiteralPath $source) {
  if ((Get-FileHash -LiteralPath $source).Hash -ne (Get-FileHash -LiteralPath $original).Hash) { throw 'Source identity mismatch' }
 } else { Copy-Item -LiteralPath $original -Destination $source }
 $target = Join-Path $normalizedDir ($asset.Name + '.png')
 $count = [GrainOutlinePalette]::Export($source,$target)
 Write-Output ($asset.Name + ': normalized outline pixels=' + $count)
}
