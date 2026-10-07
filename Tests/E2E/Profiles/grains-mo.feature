Feature: Grains real-provider migration smoke - mo

  Scenario: Grains mo loads the requested real providers
    Then the real MO Grains providers are active

  Scenario: Grains mo primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo optional cold tolerance resolves
    Then Grains cold tolerance extensions are absent

  Scenario: Grains mo New Village definition resolves
    Then loaded New Village scenario matches the start design

  @quickstart:AmjNewVillageQuickstart
  Scenario: Grains mo New Village starts
    Then New Village starts with five villagers and the designed supplies

  Scenario: Grains mo wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve
