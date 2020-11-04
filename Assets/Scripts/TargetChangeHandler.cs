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

    public void ImageTargetFoundHandler(string name)
    {
        if(debug_active)
        {
            Logger.Log("Image target - " + name + " - was FOUND.");
        }

        if(name == "Base")
        {
            GameController.Instance.basePlaced = true;
        }
        
    }

    public void ImageTargetLostHandler(string name)
    {
        if (debug_active)
        {
            Logger.Log("Image target - " + name + " - was LOST.");
        }
        
        if(name == "Base")
        {
            GameController.Instance.basePlaced = false;
        }
        
    }
}
