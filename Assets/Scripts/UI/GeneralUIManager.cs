using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GeneralUIManager : MonoBehaviour {
    public GameObject playUI;
    public GameObject timerLabel;
    Text timerText;
    public GameObject visualizationTab;
    public GameObject addMenu;
    public GameObject navigationButton;
    public GameObject connectionMenu;

    void Start()
    {
        timerText = timerLabel.GetComponent<Text>();
        TogglePlayUI();
    }

    public void TogglePlayUI()
    {
        playUI.SetActive(true);
    }

    public void ToggleConnectionMenu() {
        connectionMenu.SetActive(true);
    }

    public void ToggleOffMenus()
    {
        playUI.SetActive(false);
    }

    public void SetTime(string timerec)
    {
        timerText.text = timerec;
    }
}
