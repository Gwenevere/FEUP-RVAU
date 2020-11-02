using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GeneralUIManager : MonoBehaviour {
    public GameObject playUI;
    public GameObject timerLabel;
    Text timerText;
    public GameObject MenuUI;
    public GameObject addMenu;
    public GameObject navigationButton;
    public GameObject connectionMenu;

    void Start()
    {
        timerText = timerLabel.GetComponent<Text>();
        ToggleMenuUI();
    }

    public void TogglePlayUI()
    {
        ToggleOffMenus();
        playUI.SetActive(true);
    }

    public void StartGame()
    {
        TogglePlayUI();
    }

    public void ToggleMenuUI()
    {
        ToggleOffMenus();
        MenuUI.SetActive(true);
    }

    public void ToggleConnectionMenu() {
        connectionMenu.SetActive(true);
    }

    public void ToggleOffMenus()
    {
        MenuUI.SetActive(false);
        playUI.SetActive(false);
    }

    public void SetTime(string timerec)
    {
        timerText.text = timerec;
    }
}
