﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Tower : MonoBehaviour
{
    public int health = 1000;
    public int max_health = 1000;
    public HealthBar healthBar;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
    }

    void TakeDamage(int damage)
    {
        health -= damage;
        healthBar.SetHealth(health);    
    }
}
