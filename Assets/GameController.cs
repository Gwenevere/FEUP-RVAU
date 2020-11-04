using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameController : MonoBehaviour
{
    private static GameController _instance;

    public static GameController Instance { get { return _instance; } }

    private void Awake()
    {
        if (_instance != null && _instance != this)
        {
            Destroy(this.gameObject);
        } else {
            _instance = this;
        }
    }

    public GameObject enemy_controller;
    private EnemySpawner enemy_spawner;
    GameObject GUI;
    GeneralUIManager UImanager;
    [HideInInspector]
    public float gameTimer = 0;
    [HideInInspector]
    public int current_wave = 1;
    [HideInInspector]
    public bool playing = false;
    [HideInInspector]
    private bool basePlaced; // Game starts only if base image target was detected
    public int numTurrets = 1;
    public int money = 0;
   
    // Start is called before the first frame update
    void Start()
    {
        basePlaced = true;      // eliminar
        GUI = GameObject.Find("GUI");
        enemy_spawner = enemy_controller.GetComponent<EnemySpawner>();
        UImanager = GUI.GetComponent<GeneralUIManager>();
        //StartGame();
    }

    // Update is called once per frame
    void Update()
    {
        gameTimer += Time.deltaTime;
        if(playing)
        {
            UpdateUITimer();
        }
    }

    public void StartGame()
    {
        Debug.Log(basePlaced);
        if(basePlaced)
        {
            UImanager.TogglePlayUI();
            Logger.Log("Base position");
            Logger.Log(GameObject.Find("Base").transform.position);
            playing = true;
            enemy_spawner.StartWave();
        } else {
            UImanager.NoBaseWarning();
        }
    }

    public void LoseGame()
    {
        enemy_spawner.StopWave();
        playing = false;
        Logger.Log("GAME OVER");
        UImanager.ToggleGameOverUI();
        
    }

    public void NextWave()
    {
        Debug.Log("Wave " + current_wave +" ended");
        if(!playing)
        {
            return;
        }
        current_wave++;
        //  Shop?
        enemy_spawner.StartWave();
        Debug.Log("Wave " + current_wave +" started");
    }
     void UpdateUITimer() {
 
        var minutes = gameTimer / 60; //Divide the guiTime by sixty to get the minutes.
        var seconds = gameTimer % 60;//Use the euclidean division for the seconds.
        var fraction = (gameTimer * 100) % 100;

        UImanager.SetTime(string.Format ("{0:00} : {1:00}", minutes, seconds));
        //timerLabel.GetComponent<Text>() = string.Format ("{0:00} : {1:00}", minutes, seconds);
     }
}
