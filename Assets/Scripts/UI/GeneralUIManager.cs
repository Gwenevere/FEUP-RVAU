using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GeneralUIManager : MonoBehaviour {
    public GameObject playUI;
    public GameObject timerLabel;
    Text timerText;
    public GameObject MenuUI;
    public GameObject gameOverUI;
    private MenuUI Menu;
    public GameObject addMenu;
    public GameObject navigationButton;
    public GameObject connectionMenu;

    void Start()
    {
        Menu = MenuUI.GetComponent<MenuUI>();
        
        timerText = timerLabel.GetComponent<Text>();
        ToggleMenuUI();
    }

    public void TogglePlayUI()
    {
        ToggleOffMenus();
        playUI.SetActive(true);
    }

    public void ToggleGameOverUI()
    {
        ToggleOffMenus();
        gameOverUI.SetActive(true);
        
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
        gameOverUI.SetActive(false);
    }

    public void SetTime(string timerec)
    {
        timerText.text = timerec;
    }

    public void ExitGame()
    {
        Application.Quit();
    }

    public void NoBaseWarning()
    {
        Menu.NoBaseWarning();
    }
}
