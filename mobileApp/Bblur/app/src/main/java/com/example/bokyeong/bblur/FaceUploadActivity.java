package com.example.bokyeong.bblur;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.InputStream;

public class FaceUploadActivity extends AppCompatActivity implements View.OnClickListener {

    private Button buttonChoosePhoto; // 사진 선택 버튼
    private Button buttonUploadPhoto; // 업로드 버튼
    private TextView textView;
    private TextView textViewResponse;
    private Button buttonDelete;
    private ImageView myface_preview_main; //사진 미리보기

    private static final int SELECT_PHOTO = 3;

    private  String selectedPath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_face_upload);

        buttonChoosePhoto = (Button) findViewById(R.id.buttonChoosePhoto);
        buttonUploadPhoto = (Button) findViewById(R.id.buttonUploadPhoto);
        buttonDelete = (Button) findViewById(R.id.buttonDelete);

        textView = (TextView) findViewById(R.id.textView);
        textViewResponse = (TextView) findViewById(R.id.textViewResponse);
        myface_preview_main = (ImageView) findViewById(R.id.myface_preview_main);

        buttonChoosePhoto.setOnClickListener(this);
        buttonUploadPhoto.setOnClickListener(this);
        buttonDelete.setOnClickListener(this);
    }

    private void chooseVideo() {
        Intent intent = new Intent();
        intent.setAction(Intent.ACTION_PICK);
        intent.setType(android.provider.MediaStore.Images.Media.CONTENT_TYPE);
        startActivityForResult(Intent.createChooser(intent, "Select a Photo "), SELECT_PHOTO);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == RESULT_OK) {
            if (requestCode == SELECT_PHOTO) {
                System.out.println("SELECT_PHOTO");
                Uri selectedImageUri = data.getData();
                selectedPath = getPath(selectedImageUri);
                try {
                    //선택한 이미지에서 비트맵 생성
                    InputStream inputStream = getContentResolver().openInputStream(data.getData());
                    Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
                    inputStream.close();

                    //이미지 표시
                    myface_preview_main.setImageBitmap(bitmap);

                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        }
    }

    public String getPath(Uri uri) {
        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
        cursor.moveToFirst();
        String document_id = cursor.getString(0);
        document_id = document_id.substring(document_id.lastIndexOf(":") + 1);
        cursor.close();

        cursor = getContentResolver().query(
                android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                null, MediaStore.Images.Media._ID + " = ? ", new String[]{document_id}, null);
        cursor.moveToFirst();
        String path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
        cursor.close();

        return path;
    }

    private void uploadPhoto() {

        if (selectedPath == null) {
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("선택된 사진이 없습니다")
                    .setMessage("사진을 먼저 선택하세요")
                    .setNegativeButton("확 인", null).setCancelable(false);

            AlertDialog alert = builder.create();
            alert.show();

        } else {
            class UploadVideo extends AsyncTask<Void, Void, String> {

                ProgressDialog uploading;

                @Override
                protected void onPreExecute() {
                    super.onPreExecute();
                    uploading = ProgressDialog.show(FaceUploadActivity.this, "Uploading File", "Please wait...", false, false);
                }

                @Override
                protected void onPostExecute(String s) {
                    super.onPostExecute(s);
                    uploading.dismiss();
                    Toast toast = Toast.makeText(getApplicationContext(), "처리 제외 대상이 저장되었습니다.", Toast.LENGTH_LONG); toast.show();

                }

                @Override
                protected String doInBackground(Void... params) {
                    UploadNoEdit u = new UploadNoEdit();
                    String msg = u.upLoad2Server(selectedPath);
                    return msg;
                }
            }
            UploadVideo uv = new UploadVideo();
            uv.execute();
        }
    }


    private void deletePhoto() {
        class DeletePhoto extends AsyncTask<Void, Void, String> {

            ProgressDialog deleting;

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                deleting = ProgressDialog.show(FaceUploadActivity.this, "Deleting File", "Please wait...", false, false);
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                deleting.dismiss();
                Toast.makeText(getApplicationContext(), "모든 제외 대상 사진이 삭제되었습니다." , Toast.LENGTH_LONG).show();

            }

            @Override
            protected String doInBackground(Void... params) {
                Delete u = new Delete();
                String msg = u.deletePhoto();
                return msg;

            }
        }
        DeletePhoto uv = new DeletePhoto();
        uv.execute();


    }







        @Override
    public void onClick(View v) {
        if (v == buttonChoosePhoto) {
            chooseVideo();
        }

        if (v == buttonUploadPhoto) {
            uploadPhoto();
        }

        if (v == buttonDelete){
            deletePhoto();
        }
    }
}