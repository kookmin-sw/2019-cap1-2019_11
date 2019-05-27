package com.example.bokyeong.bblur;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.PowerManager;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.net.URLConnection;

public class MyUploadActivity extends AppCompatActivity implements View.OnClickListener{

    private Button buttonChoose; // 비디오 선택 버튼
    private Button buttonUpload; // 업로드 버튼
    private Button buttonDownload; // 다운로드 버튼
    private TextView textView;
    private TextView textViewResponse;
    private VideoView video_preview_main2;

    private static final int SELECT_VIDEO = 3;

    private  String selectedPath;

    private ProgressDialog progressBar;
    private File outputFile;
    private File filePath;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my_upload);

        buttonChoose = (Button) findViewById(R.id.buttonChoose);
        buttonUpload = (Button) findViewById(R.id.buttonUpload);
        buttonDownload = (Button) findViewById(R.id.buttonDownload);

        textView = (TextView) findViewById(R.id.textView);
        textViewResponse = (TextView) findViewById(R.id.textViewResponse);
//        video_preview_main2 = (VideoView) findViewById(R.id.video_preview_main2);

        buttonChoose.setOnClickListener(this);
        buttonUpload.setOnClickListener(this);
        buttonDownload.setOnClickListener(this);

        progressBar=new ProgressDialog(MyUploadActivity.this);
        progressBar.setMessage("다운로드 중");
        progressBar.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
        progressBar.setIndeterminate(true);
        progressBar.setCancelable(true);

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
                Toast toast = Toast.makeText(getApplicationContext(), "동영상이 선택되었습니다. 업로드를 진행하세요.", Toast.LENGTH_LONG); toast.show();

            }
            // VideoView : 동영상을 재생하는 뷰
            //VideoView vv = (VideoView) findViewById(R.id.video_preview_main2);

            // MediaController : 특정 View 위에서 작동하는 미디어 컨트롤러 객체
            /*MediaController mc = new MediaController(this);
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
            video_preview_main2.start(); // 동영상 재생*/
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


    private void downloadVideo() {
        final String fileURL = "http://52.79.176.116/outputs/finalvideo.mp4";

        filePath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        outputFile = new File(filePath, "s.mp4");

        if (outputFile.exists()) {
            AlertDialog.Builder builder = new AlertDialog.Builder(MyUploadActivity.this);
            builder.setTitle("다운로드");
            builder.show();
        } else {
            final DownloadFilesTask downloadTask = new DownloadFilesTask(MyUploadActivity.this);
            downloadTask.execute(fileURL);

            progressBar.setOnCancelListener(new DialogInterface.OnCancelListener() {
                @Override
                public void onCancel(DialogInterface dialog) {
                    downloadTask.cancel(true);
                }
            });
        }

    }

    private class DownloadFilesTask extends AsyncTask<String, String, Long> {
        private Context context;
        private PowerManager.WakeLock mWakeLock;

        public DownloadFilesTask(Context context) {
            this.context = context;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

            PowerManager pm = (PowerManager) context.getSystemService(Context.POWER_SERVICE);
            mWakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, getClass().getName());
            mWakeLock.acquire();

            progressBar.show();
        }

        @Override
        protected Long doInBackground(String... string_url) {
            int count;
            long FileSize = -1;
            InputStream input = null;
            OutputStream output = null;
            URLConnection connection = null;

            try {
                URL url = new URL(string_url[0]);
                connection = url.openConnection();
                connection.connect();

                FileSize = connection.getContentLength();

                input = new BufferedInputStream(url.openStream(), 81920);

                filePath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                outputFile = new File(filePath, "finish.mp4"); //파일명까지 포함함 경로의 File 객체 생성

                // SD카드에 저장하기 위한 Output stream
                output = new FileOutputStream(outputFile);


                byte data[] = new byte[1024];
                long downloadedSize = 0;

                while ((count = input.read(data)) != -1) {
                    //사용자가 BACK 버튼 누르면 취소가능
                    if (isCancelled()) {
                        input.close();
                        return Long.valueOf(-1);
                    }

                    downloadedSize += count;

                    if (FileSize > 0) {
                        float per = ((float) downloadedSize / FileSize) * 100;
                        String str = "Downloaded " + downloadedSize + "KB / " + FileSize + "KB (" + (int) per + "%)";
                        publishProgress("" + (int) ((downloadedSize * 100) / FileSize), str);

                    }

                    //파일에 데이터를 기록합니다.
                    output.write(data, 0, count);
                }

                // Flush output
                output.flush();

                // Close streams
                output.close();
                input.close();


            } catch (Exception e) {
                Log.e("error : ", e.getMessage());
            } finally {
                try {
                    if (output != null)
                        output.close();
                    if (input != null)
                        input.close();
                } catch (IOException ignored) {
                }
                mWakeLock.release();
            }

            return FileSize;
        }

        @Override
        protected void onProgressUpdate(String... progress) { //4
            super.onProgressUpdate(progress);

            // if we get here, length is known, now set indeterminate to false
            progressBar.setIndeterminate(false);
            progressBar.setMax(100);
            progressBar.setProgress(Integer.parseInt(progress[0]));
            progressBar.setMessage(progress[1]);
        }

        @Override
        protected void onPostExecute(Long size) { //5
            super.onPostExecute(size);

            progressBar.dismiss();

            if ( size > 0) {
                Toast.makeText(getApplicationContext(), "다운로드 완료되었습니다. 파일 크기=" + size.toString(), Toast.LENGTH_LONG).show();

                Intent mediaScanIntent = new Intent( Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
                mediaScanIntent.setData(Uri.fromFile(outputFile));
                sendBroadcast(mediaScanIntent);

//                playVideo(outputFile.getPath());

            }
            else
                Toast.makeText(getApplicationContext(), "다운로드 에러", Toast.LENGTH_LONG).show();
        }


    }


//        downloadTask.execute("http://52.79.176.116/outputs/finalvideo.mp4");


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