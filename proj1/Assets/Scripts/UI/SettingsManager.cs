using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SettingsManager : MonoBehaviour {
    public bool soundActive = true;
    public GameObject soundButton;
    public Sprite soundOnSprite;
    public Sprite soundOffSprite;

    public void ToggleSound() {
        soundActive = !soundActive;

        if (soundActive) {
            soundButton.GetComponent<Image>().sprite = soundOnSprite;
        } else {
            soundButton.GetComponent<Image>().sprite = soundOffSprite;
        }
    }
}
