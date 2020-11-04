using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class GeneralUIManager : MonoBehaviour {
    Text numberKillsText;
    Text timerText;
    Text levelNumberText;
    private GameObject nextLevelButton;
    private MenuUI Menu;
    public GameObject playUI;
    public GameObject timerLabel;
    public GameObject numberKillsLabel;
    public GameObject MenuUI;
    public GameObject gameOverUI;
    public GameObject pauseUI;
    public GameObject numberLevelLabel;
    public GameObject NextLevel;
    public GameObject addMenu;
    public GameObject navigationButton;
    public GameObject connectionMenu;
    private GameObject nextButton;
    private Coroutine fadeCoroutine;

    void Start()
    {
        Menu = MenuUI.GetComponent<MenuUI>();
        
        timerText = timerLabel.GetComponent<Text>();
        numberKillsText = numberKillsLabel.GetComponent<Text>();
        levelNumberText = numberLevelLabel.GetComponent<Text>();
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

    public void TogglePauseUI()
    {
        ToggleOffMenus();
        pauseUI.SetActive(true);
    }

  
    public void DisablePauseUI()
    { 
        pauseUI.SetActive(false);
    }

    public void ToggleConnectionMenu() {
        connectionMenu.SetActive(true);
    }

    public void ToggleOffMenus()
    {
        MenuUI.SetActive(false);
        playUI.SetActive(false);
        gameOverUI.SetActive(false);
        pauseUI.SetActive(false);
    }

    public void SetTime(string timerec)
    {
        timerText.text = timerec;
    }

    public void SetNextLevel(string nextlevel)
    {
        levelNumberText.text = nextlevel;
    }

    public void SetNumberKills(string killsnumber)
    {
        numberKillsText.text = killsnumber;
    }

    public void NextLevelWarning()
    {
        if (fadeCoroutine != null)
        {
            StopCoroutine(fadeCoroutine);
        }
        if (nextLevelButton != null)
        {
            GameObject.Destroy(nextLevelButton);
        }
        nextButton = Instantiate(nextLevelButton, nextLevelButton.transform.position, Quaternion.identity);
        nextButton.transform.SetParent(gameObject.transform);
        nextButton.SetActive(true);
        fadeCoroutine = StartCoroutine(FadeOutRoutine());
    }

    private IEnumerator FadeOutRoutine()
    {
        Text text = nextButton.GetComponent<Text>();
        Color originalColor = text.color;
        for (float t = 0.01f; t < 6; t += Time.deltaTime)
        {
            text.color = Color.Lerp(originalColor, Color.clear, Mathf.Min(1, t / 3));
            yield return null;
        }
        if (nextButton != null)
        {
            GameObject.Destroy(nextButton);
        }
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
