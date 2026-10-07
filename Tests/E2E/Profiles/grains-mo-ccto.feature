Feature: Grains real-provider migration smoke - mo-ccto

  Scenario: Grains mo-ccto loads the requested real providers
    Then the real MO CCTO Grains providers are active

  Scenario: Grains mo-ccto primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo-ccto optional cold tolerance resolves
    Then Grains cold tolerance extensions are present

  Scenario: Grains mo-ccto wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve

  Scenario: Grains mo-ccto six grains retain environmental niches
    Then six Grains retain environmental harvest niches

  @quickstart:AmjStageAQuickstart
  Scenario: Grains mo-ccto real harvest and flour food Bills complete
    Then Grains harvest and flour food Bills complete through real jobs
