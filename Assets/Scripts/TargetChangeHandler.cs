using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetChangeHandler : MonoBehaviour
{
    public bool debug_active;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ContentPlacedHandler()
    {
        if(debug_active)
        {
            Logger.Log(" Content placed");
        }
    }

    public void ImageTargetFoundHandler()
    {
        if(debug_active)
        {
            if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject != null)
            {
                Logger.Log("Image target - " + UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject.name + " - was FOUND.");
            }
        }

        if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject != null)
        {
            if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject.name == "Base")
            {
                GameController.Instance.basePlaced = true;
            }
        }
    }

    public void ImageTargetLostHandler()
    {
        if(debug_active)
        {
            if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject != null)
            {
                Logger.Log("Image target - " + UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject.name + " - was LOST.");
            }
        }

        if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject != null)
        {
            if(UnityEngine.EventSystems.EventSystem.current.currentSelectedGameObject.name == "Base")
            {
                GameController.Instance.basePlaced = false;
            }
        }
    }
}
