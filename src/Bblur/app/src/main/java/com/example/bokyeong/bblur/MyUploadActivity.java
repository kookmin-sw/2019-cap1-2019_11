package com.example.bokyeong.bblur;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.VideoView;

public class MyUploadActivity extends AppCompatActivity implements View.OnClickListener {

    private Button buttonChoose; // 비디오 선택 버튼
    private Button buttonUpload; // 업로드 버튼
    private TextView textView;
    private TextView textViewResponse;
    private VideoView video_preview_main2;

    private static final int SELECT_VIDEO = 3;

    private  String selectedPath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_upload);

        buttonChoose = (Button) findViewById(R.id.buttonChoose);
        buttonUpload = (Button) findViewById(R.id.buttonUpload);

        textView = (TextView) findViewById(R.id.textView);
        textViewResponse = (TextView) findViewById(R.id.textViewResponse);
        video_preview_main2 = (VideoView) findViewById(R.id.video_preview_main2);

        buttonChoose.setOnClickListener(this);
        buttonUpload.setOnClickListener(this);
    }

    private void chooseVideo() {
        Intent intent = new Intent();
        intent.setType("video/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(intent, "Select a Video "), SELECT_VIDEO);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == RESULT_OK) {
            if (requestCode == SELECT_VIDEO) {
                System.out.println("SELECT_VIDEO");
                Uri selectedImageUri = data.getData();
                selectedPath = getPath(selectedImageUri);
                textView.setText("동영상이 선택되었습니다.");
            }
            // VideoView : 동영상을 재생하는 뷰
            //VideoView vv = (VideoView) findViewById(R.id.video_preview_main2);

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
                null, MediaStore.Video.Media._ID + " = ? ", new String[]{document_id}, null);
        cursor.moveToFirst();
        String path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
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

    @Override
    public void onClick(View v) {
        if (v == buttonChoose) {
            chooseVideo();
        }

        if (v == buttonUpload) {
            uploadVideo();
        }

    }
}
