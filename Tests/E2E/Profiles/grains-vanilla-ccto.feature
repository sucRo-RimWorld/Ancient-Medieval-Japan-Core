Feature: Grains real-provider migration smoke - vanilla-ccto

  Scenario: Grains vanilla-ccto loads the requested real providers
    Then the real vanilla CCTO Grains providers are active

  Scenario: Grains vanilla-ccto primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains vanilla-ccto optional cold tolerance resolves
    Then Grains cold tolerance extensions are present
