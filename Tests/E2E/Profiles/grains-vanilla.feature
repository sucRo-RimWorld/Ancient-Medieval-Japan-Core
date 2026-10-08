Feature: Grains real-provider migration smoke - vanilla

  Scenario: Grains vanilla loads the requested real providers
    Then the real vanilla Grains providers are active

  Scenario: Grains vanilla primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains vanilla optional cold tolerance resolves
    Then Grains cold tolerance extensions are absent

  Scenario: Grains vanilla wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve

  Scenario: Grains vanilla seven grains retain environmental niches
    Then seven Grains retain environmental harvest niches

  @quickstart:AmjStageAQuickstart
  Scenario: Grains vanilla real harvest and flour food Bills complete
    Then Grains harvest and flour food Bills complete through real jobs
