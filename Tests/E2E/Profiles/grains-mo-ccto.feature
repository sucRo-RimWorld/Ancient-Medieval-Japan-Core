Feature: Grains real-provider migration smoke - mo-ccto

  Scenario: Grains mo-ccto loads the requested real providers
    Then the real MO CCTO Grains providers are active

  Scenario: Grains mo-ccto primary grain loop resolves
    Then the Grains primary grain loop resolves

  Scenario: Grains mo-ccto optional cold tolerance resolves
    Then Grains cold tolerance extensions are present

  Scenario: Grains mo-ccto New Village definition resolves
    Then loaded New Village scenario matches the start design

  @quickstart:AmjNewVillageQuickstart
  Scenario: Grains mo-ccto New Village starts
    Then New Village starts with five villagers and the designed supplies

  Scenario: Grains mo-ccto wheat flour and minimum food resolve
    Then the Grains wheat flour and minimum food chains resolve
