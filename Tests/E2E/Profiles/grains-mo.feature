Feature: Grains real-provider migration smoke - mo

  Scenario: Grains mo loads the requested real providers
    Then the real MO Grains providers are active

  Scenario: Grains mo primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo optional cold tolerance resolves
    Then Grains cold tolerance extensions are absent

  Scenario: Grains mo wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve

  Scenario: Grains mo seven grains retain environmental niches
    Then seven Grains retain environmental harvest niches

  @quickstart:AmjStageAQuickstart @timeout:270
  Scenario: Grains mo real harvest and flour food Bills complete
    Then Grains harvest and flour food Bills complete through real jobs
