Feature: Grains real-provider migration smoke - vanilla

  Scenario: Grains vanilla loads the requested real providers
    Then the real vanilla Grains providers are active

  Scenario: Grains vanilla primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains vanilla optional cold tolerance resolves
    Then Grains cold tolerance extensions are absent
