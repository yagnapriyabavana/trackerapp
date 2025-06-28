dependencies {
    implementation 'androidx.appcompat:appcompat:1.7.0'
    implementation 'com.google.android.material:material:1.11.0'
}
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION" />
<uses-feature android:name="android.hardware.sensor.stepcounter" android:required="false"/>
<uses-feature android:name="android.hardware.sensor.accelerometer" android:required="false"/>
<LinearLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:padding="16dp"
    android:gravity="center"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:id="@+id/tvSteps"
        android:text="Steps: 0"
        android:textSize="20sp"
        android:layout_margin="16dp"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <TextView
        android:id="@+id/tvDistance"
        android:text="Distance: 0.0 m"
        android:textSize="20sp"
        android:layout_margin="16dp"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <TextView
        android:id="@+id/tvCalories"
        android:text="Calories: 0 kcal"
        android:textSize="20sp"
        android:layout_margin="16dp"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

    <Button
        android:id="@+id/btnStartStop"
        android:text="Start"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />

</LinearLayout>
package com.example.steptracker

import android.Manifest
import android.content.pm.PackageManager
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.core.app.ActivityCompat
import kotlin.math.roundToInt

class MainActivity : AppCompatActivity(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var stepSensor: Sensor? = null
    private var isTracking = false
    private var totalSteps = 0

    private lateinit var tvSteps: TextView
    private lateinit var tvDistance: TextView
    private lateinit var tvCalories: TextView
    private lateinit var btnStartStop: Button

    // Constants for Estimation
    private val STRIDE_LENGTH = 0.78 // average stride length in meters
    private val CALORIES_PER_STEP = 0.04 // Rough calories burned per step

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvSteps = findViewById(R.id.tvSteps)
        tvDistance = findViewById(R.id.tvDistance)
        tvCalories = findViewById(R.id.tvCalories)
        btnStartStop = findViewById(R.id.btnStartStop)

        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        stepSensor = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR)

        requestPermission()

        btnStartStop.setOnClickListener {
            isTracking = !isTracking
            btnStartStop.text = if (isTracking) "Stop" else "Start"
            if (!isTracking) resetData()
        }
    }

    private fun requestPermission() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACTIVITY_RECOGNITION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACTIVITY_RECOGNITION), 100)
        }
    }

    override fun onResume() {
        super.onResume()
        stepSensor?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_UI)
        }
    }

    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (isTracking && event?.sensor?.type == Sensor.TYPE_STEP_DETECTOR) {
            totalSteps++
            updateUI()
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    private fun updateUI() {
        val distance = totalSteps * STRIDE_LENGTH // meters
        val calories = totalSteps * CALORIES_PER_STEP

        tvSteps.text = "Steps: $totalSteps"
        tvDistance.text = "Distance: ${String.format("%.2f", distance)} m"
        tvCalories.text = "Calories: ${calories.roundToInt()} kcal"
    }

    private fun resetData() {
        totalSteps = 0
        updateUI()
    }
}
