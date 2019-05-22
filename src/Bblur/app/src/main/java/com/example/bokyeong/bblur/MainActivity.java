package com.example.bokyeong.bblur;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements  View.OnClickListener{

    Button buttonMyUpload;
    Button buttonPhotoUpload;
    Button buttonFaceUpload;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        buttonMyUpload = (Button) findViewById(R.id.buttonMyUpload);
        buttonPhotoUpload = (Button) findViewById(R.id.buttonPhotoUpload);
        buttonFaceUpload = (Button) findViewById(R.id.buttonFaceUpload);

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
    }
}
