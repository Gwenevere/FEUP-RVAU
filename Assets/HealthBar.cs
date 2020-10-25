using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HealthBar : MonoBehaviour
{
    public GameObject _object;
    public Slider slider;
    public Gradient gradient;
    public Image fill;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetHealth(int amount)
    {
        slider.value = amount;
        fill.color = gradient.Evaluate(slider.normalizedValue);
        
    }

    public void SetMaxHealth(int new_max_health)
    {
        slider.maxValue = new_max_health;
        fill.color = gradient.Evaluate(slider.normalizedValue);
    }

    
}
