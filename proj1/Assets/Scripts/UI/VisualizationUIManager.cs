using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VisualizationUIManager : MonoBehaviour
{
    public GameObject playButton;
    public GeneralUIManager generalUIManager;
    public GameObject pauseButton;
    private bool isPaused = false;
    public GameObject resetButton;
    private bool wasProgramStarted = false;

    private List<Vector3> objectPositions = new List<Vector3>();
    private List<Quaternion> objectRotations = new List<Quaternion>();

    private List<Vector3> robotPositions = new List<Vector3>();
    private List<Quaternion> robotRotations = new List<Quaternion>();

    public void StartVisualization() {
        generalUIManager.ToggleOffMenus();
        playButton.SetActive(false);
        pauseButton.SetActive(true);

        if (isPaused) {
            Time.timeScale = 1;
            isPaused = false;

        }else{
            RecordStartPosition();
            wasProgramStarted = true;
        }

    }
    
    public void PauseVisualization() {
        generalUIManager.ToggleOffMenus();
        pauseButton.SetActive(false);
        playButton.SetActive(true);
        Time.timeScale = 0;
        isPaused = true;
    }

    public void ResetVisualization()
    {
        generalUIManager.ToggleOffMenus();
        pauseButton.SetActive(false);
        playButton.SetActive(true);

        HandleRepositioning();
    }

    public void SwitchingTabs() {

        if (wasProgramStarted) {
            
            HandleRepositioning();

            pauseButton.SetActive(false);
            playButton.SetActive(true);
        }

    }

    public void RecordStartPosition() {

        // record position
        Transform[] allObjects = GameObject.Find("ObjectParent").transform.GetComponentsInChildren<Transform>();
        foreach (Transform obj in allObjects)
        {
            objectPositions.Add(obj.position);
            objectRotations.Add(obj.rotation);
        }

        Transform[] allRobots = GameObject.Find("RobotParent").transform.GetComponentsInChildren<Transform>();
        foreach (Transform robot in allRobots)
        {
            if (!(robot.gameObject.name == "ObjectParent"))
            {
                robotPositions.Add(robot.position);
                robotRotations.Add(robot.rotation);
            }
        }
    }

    public void HandleRepositioning(){

        //stop recording
        Transform[] allObjects = GameObject.Find("ObjectParent").transform.GetComponentsInChildren<Transform>();
        foreach (Transform obj in allObjects)
        {
            obj.transform.position = objectPositions[0];
            objectPositions.RemoveAt(0);
            obj.transform.rotation = objectRotations[0];
            objectRotations.RemoveAt(0);
        }

        //change robot state

        //reset robot position
        Transform[] allRobots = GameObject.Find("RobotParent").transform.GetComponentsInChildren<Transform>();
        foreach (Transform robot in allRobots)
        {
            if (!(robot.gameObject.name == "ObjectParent"))
            {
                robot.transform.position = robotPositions[0];
                robotPositions.RemoveAt(0);
                robot.transform.rotation = robotRotations[0];
                robotRotations.RemoveAt(0);
            }
        }

        wasProgramStarted = false;

        if (isPaused) { 
            Time.timeScale = 1;
            isPaused = false;
        }

    }
    
}
