Feature: Grains real-provider migration smoke - vanilla-ccto

  Scenario: Grains vanilla-ccto loads the requested real providers
    Then the real vanilla CCTO Grains providers are active

  Scenario: Grains vanilla-ccto primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains vanilla-ccto optional cold tolerance resolves
    Then Grains cold tolerance extensions are present

  Scenario: Grains vanilla-ccto wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve

  Scenario: Grains vanilla-ccto seven grains retain environmental niches
    Then seven Grains retain environmental harvest niches

  @quickstart:AmjStageAQuickstart
  Scenario: Grains vanilla-ccto real harvest and flour food Bills complete
    Then Grains harvest and flour food Bills complete through real jobs
