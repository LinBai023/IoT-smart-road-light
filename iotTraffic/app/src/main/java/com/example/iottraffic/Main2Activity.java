package com.example.iottraffic;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import java.util.concurrent.TimeUnit;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.net.SocketTimeoutException;

public class Main2Activity extends AppCompatActivity{
    String re = "";
    ArrayList<Integer> things;

    TextView timeItems;
    TextView trafficItems;

    String echo = "";


    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        timeItems = findViewById(R.id.timeItems);
        trafficItems = findViewById(R.id.trafficItems);

        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
//        Menu menu = navigation.getMenu();
//        MenuItem menuItem = menu.getItem(1);
//        menuItem.setChecked(true);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);



        Log.v("text","sending");
        String url = "http://ec2-3-84-46-25.compute-1.amazonaws.com/";



//        call server
        while(true) {
            try {
                new CallAPI().execute(url, "getting all data from mongodb");
                if (re != "") {
                    Log.i("info", re);
                    break;
                }
            }
            catch (Exception e){
                try {
                    TimeUnit.SECONDS.sleep(3);
                } catch (InterruptedException e1) {
                    e1.printStackTrace();
                }
            }
        }


        String things = re;

        String testre = "2";
        Date date = new Date();

        trafficItems.setText(things);
        timeItems.setText(date.toString());
    }

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_home:
                    // mTextMessage.setText(R.string.title_home);
                    openActivity1();
                    return true;
                case R.id.navigation_dashboard:
                    //mTextMessage.setText(R.string.title_dashboard);
                   // openActivity2();

                    return true;
                case R.id.navigation_notifications:
                    // mTextMessage.setText(R.string.title_notifications);
                    openActivity3();
                    return true;
            }
            return false;
        }
    };

    public void openActivity1(){
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }

    public void openActivity3(){
        Intent intent = new Intent(this, Main2Activity.class);
        startActivity(intent);
    }

//    public void jumpToEdit(View view){
//        Intent intent = new Intent(this, edit_exp.class);
//        startActivity(intent);
//        //String url = "http://ec2-54-242-237-70.compute-1.amazonaws.com/";
//        //call server
//        //new CallAPI().execute(url,"edit");
//
//    }



    public class CallAPI extends AsyncTask<String, String, String> {

        @Override
        protected void onPreExecute() {

        }



        @Override
        protected String doInBackground(String... params) {
            String urlString = params[0]; // URL to call
            String data = params[1]; //data to post
            OutputStream out = null;
            String response = "";

            try {
                URL url = new URL(urlString);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setConnectTimeout(5000);
                urlConnection.setRequestMethod("POST");
                out = new BufferedOutputStream(urlConnection.getOutputStream());


                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
                Log.v("doinbackground data",data);
                writer.write(data);
                writer.flush();
                writer.close();
                out.close();


                urlConnection.connect();


                String line;
                BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                while ((line = br.readLine()) != null) {
                    //Log.v("hhh",line) ;
                    response += line;
                }

                urlConnection.disconnect();
                re = response;
            }
            catch (Exception e) {
                System.out.println(e.getMessage());
                response = "Failure";
            }
            return response;
        }

        @Override
        protected void onPostExecute(String response) {

            super.onPostExecute(response);
            Log.v("result",response);
        }
    }
}
