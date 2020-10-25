using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GeneralUIManager : MonoBehaviour {
    public GameObject playUI;
    public GameObject settingsMenu;
    public GameObject visualizationTab;
    public GameObject addMenu;
    public GameObject navigationButton;
    public GameObject connectionMenu;

    void Start()
    {
        TogglePlayUI();
    }

    public void TogglePlayUI()
    {
        playUI.SetActive(true);
    }

    public void ToggleConnectionMenu() {
        settingsMenu.SetActive(false);
        connectionMenu.SetActive(true);
    }

    public void ToggleOffMenus()
    {
        playUI.SetActive(false);
    }
}
