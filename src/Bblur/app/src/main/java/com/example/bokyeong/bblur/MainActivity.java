package com.example.bokyeong.bblur;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements  View.OnClickListener{

    Button buttonGoCamera; //카메라 액티비티로 이동 버튼
    Button buttonGoVideo; //비디오 액티비티로 이동 버튼
    Button buttonMyUpload;
    Button buttonPhotoUpload;
    Button buttonFaceUpload;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        buttonGoCamera = (Button) findViewById(R.id.buttonGoCamera);
        buttonGoVideo = (Button) findViewById(R.id.buttonGoVideo);
        buttonMyUpload = (Button) findViewById(R.id.buttonMyUpload);
        buttonPhotoUpload = (Button) findViewById(R.id.buttonPhotoUpload);
        buttonFaceUpload = (Button) findViewById(R.id.buttonFaceUpload);

        buttonGoCamera.setOnClickListener(this);
        buttonGoVideo.setOnClickListener(this);
        buttonMyUpload.setOnClickListener(this);
        buttonPhotoUpload.setOnClickListener(this);
        buttonFaceUpload.setOnClickListener(this);
    }


    private void myUpload() {
        Intent intent = new Intent(getApplicationContext(), MyUploadActivity.class);
        startActivity(intent);
    }

    private void photoUpload() {
        Intent intent = new Intent(getApplicationContext(), PhotoUploadActivity.class);
        startActivity(intent);
    }

    private void faceUpload() {
        Intent intent = new Intent(getApplicationContext(), FaceUploadActivity.class);
        startActivity(intent);
    }

    private void camera_photoUpload() {
        Intent intent = new Intent(getApplicationContext(), CameraUploadActivity.class);
        startActivity(intent);
    }

    private void camera_videoUpload() {
        Intent intent = new Intent(getApplicationContext(), VideoUploadActivity.class);
        startActivity(intent);
    }

    @Override
    public void onClick(View v) {
        if(v == buttonMyUpload) {
            myUpload();
        }
        if(v == buttonPhotoUpload) {
            photoUpload();
        }
        if(v == buttonFaceUpload) {
            faceUpload();
        }
        if(v == buttonGoCamera) {
            camera_photoUpload();
        }
        if(v == buttonGoVideo) {
            camera_videoUpload();
        }
    }
}