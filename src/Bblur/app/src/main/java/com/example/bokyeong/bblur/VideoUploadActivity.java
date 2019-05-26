package com.example.bokyeong.bblur;

import android.Manifest;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import java.util.ArrayList;

public class VideoUploadActivity extends AppCompatActivity implements View.OnClickListener {

    private Button buttonVideo; //카메라 실행
    private Button buttonUploadPhoto; // 업로드 버튼
    private VideoView video_preview_main; //미리보기
    private TextView textViewResponse;

    private static final int VIDEO_REQUEST = 101;
    private String imageFilePath;
    private Uri videoUri;

    private  String selectedPath;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.acivity_video_upload);

        buttonVideo = (Button) findViewById(R.id.buttonVideo);
        buttonUploadPhoto = (Button) findViewById(R.id.buttonUploadPhoto);
        video_preview_main = (VideoView) findViewById(R.id.video_preview_main);
        textViewResponse = (TextView) findViewById(R.id.textViewResponse);

        buttonVideo.setOnClickListener(this);
        buttonUploadPhoto.setOnClickListener(this);


        //권한체크
        TedPermission.with(getApplicationContext())
                .setRationaleMessage("카메라 권한이 필요합니다.") //카메라 권한을 거부했을 때
                .setPermissionListener(permission)
                .setDeniedMessage("거부하였습니다. 설정 > 권한에서 허용해주세요.")
                .setPermissions(Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.RECORD_AUDIO)
                .check();

        findViewById(R.id.buttonVideo).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);

                if (intent.resolveActivity(getPackageManager()) != null){
                    startActivityForResult(intent, VIDEO_REQUEST);
                }
            }
        });

        //비디오 재생
        //Uri videoUri = Uri.parse(getIntent().getExtras().getString("videoUri"));
        video_preview_main.setVideoURI(videoUri);
        video_preview_main.start();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (requestCode == VIDEO_REQUEST && resultCode == RESULT_OK){
            videoUri = data.getData();
        }
    }


    private void uploadPhoto() {
        //선택된 동영상이 없을 때 알림 창
        if (selectedPath == null) {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("선택된 동영상이 없습니다")
                    .setMessage("동영상을 먼저 선택하세요")
                    .setNegativeButton("확 인", null).setCancelable(false);

            AlertDialog alert = builder.create();
            alert.show();

        } else {
            class UploadVideo extends AsyncTask<Void, Void, String> {

                ProgressDialog uploading;

                @Override
                protected void onPreExecute() {
                    super.onPreExecute();
                    uploading = ProgressDialog.show(VideoUploadActivity.this, "Uploading File", "Please wait...", false, false);
                }

                @Override
                protected void onPostExecute(String s) {
                    super.onPostExecute(s);
                    uploading.dismiss();
                    textViewResponse.setText(Html.fromHtml("<b>Uploaded at <a href='" + s + "'>" + s + "</a></b>"));
                    textViewResponse.setMovementMethod(LinkMovementMethod.getInstance());
                }

                @Override
                protected String doInBackground(Void... params) {
                    Upload u = new Upload();
                    String msg = u.upLoad2Server(selectedPath);
                    return msg;
                }
            }
            UploadVideo uv = new UploadVideo();
            uv.execute();
        }
    }

    PermissionListener permission = new PermissionListener() {
        @Override
        public void onPermissionGranted() { //permission 허용했을 때
            Toast.makeText(getApplicationContext(), "권한이 허용됨", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onPermissionDenied(ArrayList<String> deniedPermissions) { //permission 거부했을 때
            Toast.makeText(getApplicationContext(), "권한이 거부됨", Toast.LENGTH_SHORT).show();
        }
    };

    @Override
    public void onClick(View v) {
        if (v == buttonUploadPhoto) {
            uploadPhoto();
        }

    }
}
