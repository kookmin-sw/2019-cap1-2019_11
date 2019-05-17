package com.example.bokyeong.bblur;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.VideoView;
import android.content.Intent;
import android.net.Uri;



public class VideoActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video);

        VideoView vd_view = (VideoView) findViewById(R.id.videoView);
        Intent intent = getIntent(); //이 액티비티를 부른 인텐트를 받는다.
        Uri uri = intent.getParcelableExtra("videoUri");

        vd_view.setVideoURI(Uri.parse(String.valueOf(uri)));
        vd_view.requestFocus();

        vd_view.start();
    }

    public void cancelSelectVideo(View v) {
        finish(); //액티비티 종료, 메인화면으로 돌아가기
    }
}