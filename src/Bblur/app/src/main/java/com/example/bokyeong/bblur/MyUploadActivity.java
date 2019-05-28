package com.example.bokyeong.bblur;

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
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.BufferedInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.net.URLConnection;

public class MyUploadActivity extends AppCompatActivity implements View.OnClickListener{

    private Button buttonChoose; // 비디오 선택 버튼
    private Button buttonUpload; // 업로드 버튼
    private Button buttonDownload; // 다운로드 버튼
    private VideoView video_preview_main2;

    private static final int SELECT_VIDEO = 3;

    private  String selectedPath;

    private ProgressDialog pDialog;
    public static final int progress_bar_type = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_upload);

        buttonChoose = (Button) findViewById(R.id.buttonChoose);
        buttonUpload = (Button) findViewById(R.id.buttonUpload);
        buttonDownload = (Button) findViewById(R.id.buttonDownload);

        video_preview_main2 = (VideoView) findViewById(R.id.video_preview_main2);

        buttonChoose.setOnClickListener(this);
        buttonUpload.setOnClickListener(this);
        buttonDownload.setOnClickListener(this);
    }

    private void chooseVideo() {
        Intent intent = new Intent();
        intent.setAction(Intent.ACTION_PICK);
        intent.setType(android.provider.MediaStore.Video.Media.CONTENT_TYPE);
        startActivityForResult(Intent.createChooser(intent, "Select a Video "), SELECT_VIDEO);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == RESULT_OK) {
            if (requestCode == SELECT_VIDEO) {
                System.out.println("SELECT_VIDEO");
                Uri selectedImageUri = data.getData();
                selectedPath = getPath(selectedImageUri);
                Toast toast = Toast.makeText(getApplicationContext(), "동영상이 선택되었습니다.", Toast.LENGTH_SHORT); toast.show();

            }

            // VideoView : 동영상을 재생하는 뷰
            VideoView vv = (VideoView) findViewById(R.id.video_preview_main2);

            // MediaController : 특정 View 위에서 작동하는 미디어 컨트롤러 객체
            MediaController mc = new MediaController(this);
            video_preview_main2.setMediaController(mc); // Video View 에 사용할 컨트롤러 지정

            String path = Environment.getExternalStorageDirectory()
                    .getAbsolutePath(); // 기본적인 절대경로 얻어오기


            // 절대 경로 = SDCard 폴더 = "stroage/emulated/0"
            //          ** 이 경로는 폰마다 다를수 있습니다.**
            // 외부메모리의 파일에 접근하기 위한 권한이 필요 AndroidManifest.xml에 등록

            video_preview_main2.setVideoPath(""+selectedPath);
            // VideoView 로 재생할 영상
            // 아까 동영상 [상세정보] 에서 확인한 경로
            video_preview_main2.requestFocus(); // 포커스 얻어오기
            video_preview_main2.start(); // 동영상 재생
        }
    }

    public String getPath(Uri uri) {
        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
        cursor.moveToFirst();
        String document_id = cursor.getString(0);
        document_id = document_id.substring(document_id.lastIndexOf(":") + 1);
        cursor.close();

        cursor = getContentResolver().query(
                android.provider.MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
                null, MediaStore.Images.Media._ID + " = ? ", new String[]{document_id}, null);
        cursor.moveToFirst();
        String path = cursor.getString(cursor.getColumnIndex(MediaStore.Video.Media.DATA));
        cursor.close();

        return path;
    }

    private void uploadVideo() {
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
                    uploading = ProgressDialog.show(MyUploadActivity.this, "Uploading File", "Please wait...", false, false);
                }

                @Override
                protected void onPostExecute(String s) {
                    super.onPostExecute(s);
                    uploading.dismiss();
                    Toast toast = Toast.makeText(getApplicationContext(), "편집이 완료되었습니다.", Toast.LENGTH_SHORT); toast.show();
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

    private void downloadVideo() {

        new DownloadFileFromURL().execute("http://52.79.176.116/outputs/finalvideo.mp4");

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

                int lengthOfFile = connection.getContentLength();

                // 파일 다운로드
                InputStream input = new BufferedInputStream(url.openStream(), 8192);

                // 저장될 파일
                OutputStream output = new FileOutputStream(Environment
                        .getExternalStorageDirectory().toString()
                        + "/DCIM/Camera/video_" + System.currentTimeMillis() +".mp4");

                byte data[] = new byte[1024*1024];

                long total = 0;

                while ((count = input.read(data)) != -1) {
                    total += count;
                    publishProgress("" + (int) ((total * 100) / lengthOfFile));

                    output.write(data, 0, count);
                }

                output.flush();

                output.close();
                input.close();


            } catch (Exception e) {
                Log.e("Error: ", e.getMessage());
            }

            return null;
        }

        protected void onProgressUpdate(String... progress) {
            // setting progress percentage
            pDialog.setProgress(Integer.parseInt(progress[0]));
        }

        @Override
        protected void onPostExecute(String file_url) {
            // dismiss the dialog after the file was downloaded
            dismissDialog(progress_bar_type);
            Toast toast = Toast.makeText(getApplicationContext(), "다운로드가 완료되었습니다.", Toast.LENGTH_SHORT); toast.show();


        }
    }


    @Override
    public void onClick(View v) {
        if (v == buttonChoose) {
            chooseVideo();
        }

        if (v == buttonUpload) {
            uploadVideo();
        }

        if(v == buttonDownload) {
            downloadVideo();
        }
    }
}