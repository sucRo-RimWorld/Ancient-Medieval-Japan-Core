Feature: Grains real-provider migration smoke - mo-ccto

  Scenario: Grains mo-ccto loads the requested real providers
    Then the real MO CCTO Grains providers are active

  Scenario: Grains mo-ccto primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo-ccto optional cold tolerance resolves
    Then Grains cold tolerance extensions are present
