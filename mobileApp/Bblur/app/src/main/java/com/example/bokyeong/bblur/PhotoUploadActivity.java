package com.example.bokyeong.bblur;

import android.app.AlertDialog;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class PhotoUploadActivity extends AppCompatActivity implements View.OnClickListener {

    private Button buttonChoosePhoto; // 사진 선택 버튼
    private Button buttonUploadPhoto; // 업로드 버튼
    private Button buttonDownloadPhoto;
    private ImageView photo_preview_main; //사진 미리보기

    private static final int SELECT_PHOTO = 3;

    private  String selectedPath;

    private ProgressDialog pDialog;
    public static final int progress_bar_type = 0;

    Bitmap bitmap;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_photo_upload);

        buttonChoosePhoto = (Button) findViewById(R.id.buttonChoosePhoto);
        buttonUploadPhoto = (Button) findViewById(R.id.buttonUploadPhoto);
        buttonDownloadPhoto = (Button) findViewById(R.id.buttonDownloadPhoto);

        photo_preview_main = (ImageView) findViewById(R.id.photo_preview_main);

        buttonChoosePhoto.setOnClickListener(this);
        buttonUploadPhoto.setOnClickListener(this);
        buttonDownloadPhoto.setOnClickListener(this);

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
                Toast toast = Toast.makeText(getApplicationContext(), "사진이 선택되었습니다.", Toast.LENGTH_SHORT); toast.show();

                try {
                    //선택한 이미지에서 비트맵 생성
                    InputStream inputStream = getContentResolver().openInputStream(data.getData());
                    Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
                    inputStream.close();

                    //이미지 표시
                    photo_preview_main.setImageBitmap(bitmap);

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
        //선택된 사진이 없을 때 알림 창
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
                    uploading = ProgressDialog.show(PhotoUploadActivity.this, "Uploading File", "Please wait...", false, false);
                }

                @Override
                protected void onPostExecute(String s) {
                    super.onPostExecute(s);
                    uploading.dismiss();

                    Thread mThread = new Thread() {
                        @Override
                        public void run() {
                            try {
                                URL url = new URL("http://52.79.176.116/outputs/final.jpg");

                                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                                conn.setDoInput(true); // 서버 응답 수신
                                conn.connect();

                                InputStream is = conn.getInputStream();
                                bitmap = BitmapFactory.decodeStream(is);
                            } catch (MalformedURLException e) {
                                e.printStackTrace();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }

                        }
                    };

                    mThread.start();
                    try {
                        mThread.join();
                        photo_preview_main.setImageBitmap(bitmap);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }


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

    private void downloadPhoto() {

        new DownloadFileFromURL().execute("http://52.79.176.116/outputs/final.jpg");

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
                        + "/DCIM/Camera/img_" + System.currentTimeMillis() +".jpg");

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
        if (v == buttonChoosePhoto) {
            chooseVideo();
        }

        if (v == buttonUploadPhoto) {
            uploadPhoto();
        }

        if(v == buttonDownloadPhoto) {
            downloadPhoto();

        }

    }
}