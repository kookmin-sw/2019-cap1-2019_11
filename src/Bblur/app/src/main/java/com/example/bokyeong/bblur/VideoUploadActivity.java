package com.example.bokyeong.bblur;

import android.Manifest;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import java.io.BufferedInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

public class VideoUploadActivity extends AppCompatActivity implements View.OnClickListener {

    private Button buttonVideo; //카메라 실행
    private Button buttonUploadPhoto; // 업로드 버튼
    private Button buttonDownload;
    private VideoView video_preview_main; //미리보기
    private TextView textView_video;
    private TextView textViewResponse;

    private static final int VIDEO_REQUEST = 101;
    private String imageFilePath;
    private Uri videoUri;

    private  String selectedPath;
    private ProgressDialog pDialog;
    public static final int progress_bar_type = 0;


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.acivity_video_upload);

        buttonVideo = (Button) findViewById(R.id.buttonVideo);
        buttonUploadPhoto = (Button) findViewById(R.id.buttonUploadPhoto);
        buttonDownload = (Button) findViewById(R.id.buttonDownload);
        video_preview_main = (VideoView) findViewById(R.id.video_preview_main);
        textView_video = (TextView) findViewById(R.id.textView_video);
        textViewResponse = (TextView) findViewById(R.id.textViewResponse);

        buttonVideo.setOnClickListener(this);
        buttonUploadPhoto.setOnClickListener(this);
        buttonDownload.setOnClickListener(this);


        findViewById(R.id.buttonVideo).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //권한체크
                TedPermission.with(getApplicationContext())
                        .setRationaleMessage("카메라 권한이 필요합니다.") //카메라 권한을 거부했을 때
                        .setPermissionListener(permission)
                        .setDeniedMessage("거부하였습니다. 설정 > 권한에서 허용해주세요.")
                        .setPermissions(Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.RECORD_AUDIO)
                        .check();
                Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);

                if (intent.resolveActivity(getPackageManager()) != null){
                    startActivityForResult(intent, VIDEO_REQUEST);
                }
            }
        });

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (requestCode == VIDEO_REQUEST && resultCode == RESULT_OK){
            videoUri = data.getData();
            System.out.println("RECORDING_VIDEO");
            Uri selectedImageUri = data.getData();
            selectedPath = getPath(selectedImageUri);
            textView_video.setText("동영상이 선택되었습니다.");
        }

        MediaController mc = new MediaController(this);
        video_preview_main.setMediaController(mc); // Video View 에 사용할 컨트롤러 지정

        String path = Environment.getExternalStorageDirectory()
                .getAbsolutePath(); // 기본적인 절대경로 얻어오기


        // 절대 경로 = SDCard 폴더 = "stroage/emulated/0"
        //          ** 이 경로는 폰마다 다를수 있습니다.**
        // 외부메모리의 파일에 접근하기 위한 권한이 필요 AndroidManifest.xml에 등록

        video_preview_main.setVideoPath(""+selectedPath);
        // VideoView 로 재생할 영상
        // 아까 동영상 [상세정보] 에서 확인한 경로
        video_preview_main.requestFocus(); // 포커스 얻어오기
        video_preview_main.start(); // 동영상 재생
    }

    public String getPath(Uri uri) {
        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
        cursor.moveToFirst();
        String document_id = cursor.getString(0);
        document_id = document_id.substring(document_id.lastIndexOf(":") + 1);
        cursor.close();

        cursor = getContentResolver().query(
                android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
                null, MediaStore.Video.Media._ID + " = ? ", new String[]{document_id}, null);
        cursor.moveToFirst();
        String path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
        cursor.close();

        return path;
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

    private void downloadPhoto() {

        new PhotoUploadActivity.DownloadFileFromURL().execute("http://52.79.176.116/outputs/final.jpg");

    }

    @Override
    protected Dialog onCreateDialog(int id) {
        switch (id) {
            case progress_bar_type:
                pDialog = new ProgressDialog(this);
                pDialog.setMessage("Downloading file. Please wait...");
                pDialog.setIndeterminate(false);
                pDialog.setMax(100);
                pDialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
                pDialog.setCancelable(true);
                pDialog.show();
                return pDialog;
            default:
                return null;
        }
    }

    class DownloadFileFromURL extends AsyncTask<String, String, String> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            showDialog(progress_bar_type);
        }

        @Override
        protected String doInBackground(String... f_url) {
            int count;
            try {
                URL url = new URL(f_url[0]);
                URLConnection connection = url.openConnection();
                connection.connect();

                // this will be useful so that you can show a tipical 0-100%
                // progress bar
                int lengthOfFile = connection.getContentLength();

                // download the file
                InputStream input = new BufferedInputStream(url.openStream(),
                        8192);

                // Output stream
                OutputStream output = new FileOutputStream(Environment
                        .getExternalStorageDirectory().toString()
                        + "/444.jpg");

                byte data[] = new byte[1024];

                long total = 0;

                while ((count = input.read(data)) != -1) {
                    total += count;
                    publishProgress("" + (int) ((total * 100) / lengthOfFile));

                    output.write(data, 0, count);
                }

                // flushing output
                output.flush();

                // closing streams
                output.close();
                input.close();


            } catch (Exception e) {
                Log.e("Error: ", e.getMessage());
            }

            return null;
        }

        /**
         * Updating progress bar
         * */
        protected void onProgressUpdate(String... progress) {
            // setting progress percentage
            pDialog.setProgress(Integer.parseInt(progress[0]));
        }

        /**
         * After completing background task Dismiss the progress dialog
         * **/
        @Override
        protected void onPostExecute(String file_url) {
            // dismiss the dialog after the file was downloaded
            dismissDialog(progress_bar_type);

        }
    }

    @Override
    public void onClick(View v) {
        if (v == buttonUploadPhoto) {
            uploadPhoto();
        }
        if(v == buttonDownload) {
            downloadPhoto();

        }

    }
}
