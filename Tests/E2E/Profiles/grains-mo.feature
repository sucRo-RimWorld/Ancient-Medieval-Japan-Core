Feature: Grains real-provider migration smoke - mo

  Scenario: Grains mo loads the requested real providers
    Then the real MO Grains providers are active

  Scenario: Grains mo primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo optional cold tolerance resolves
    Then Grains cold tolerance extensions are absent
