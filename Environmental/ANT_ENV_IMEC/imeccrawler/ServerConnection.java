/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;
import javax.net.ssl.X509TrustManager;

/**
 *
 * @author gilman
 */
public class ServerConnection {
    private static ServerConnection serverConnection_instance = null; 
    private SSLSocketFactory socket_factory;
    
    public static ServerConnection getInstance(String ignore) 
    { 
        if (serverConnection_instance == null) 
            serverConnection_instance = new ServerConnection(ignore); 
        return serverConnection_instance; 
    } 
    
    private ServerConnection(String ignore){
        try{
            this.socket_factory = getSSLContext(ignore).getSocketFactory();
        }catch(Exception ex){
            ex.printStackTrace();
        }
              
    }
    
   private SSLContext getSSLContext(String ignore) throws Exception {
    SSLContext sslContext = SSLContext.getInstance("SSL");
    if(ignore.equalsIgnoreCase("ignore")){
        //ignore certificate
        TrustManager[] trustManagers = new TrustManager[] { new X509TrustManager() {
            @Override
            public java.security.cert.X509Certificate[] getAcceptedIssuers() { return null; }
            @Override
            public void checkClientTrusted(X509Certificate[] certs, String authType) { }
            @Override
            public void checkServerTrusted(X509Certificate[] certs, String authType) { }
         } };
        
        sslContext.init(null, trustManagers, new java.security.SecureRandom());
        
    } else if(ignore.equalsIgnoreCase("check")) {
        //checks and adds for the current session (not written to the permanent store)
        TrustManager[] trustManagers = new TrustManager[] { 
            new ReloadableX509TrustManager(false) 
        };
        sslContext.init(null, trustManagers, null);
    } else {
         //writes to permanent store
        TrustManager[] trustManagers = new TrustManager[] { 
            new ReloadableX509TrustManager(true) 
        };
      sslContext.init(null, trustManagers, null);
    }
    return sslContext;
    
   }
   
   public String sendGet(String url, String token){
        String returnString ="";
        try{
            URL auth = new URL(url);
            HttpsURLConnection connection = (HttpsURLConnection) auth.openConnection();
            connection.setSSLSocketFactory(socket_factory);
            //Headers
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Authorization", "Bearer "+token);
            connection.setRequestProperty("Content-Type", "application/json");           
            connection.connect();
            //reading reply
            BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line;
            while ((line = rd.readLine()) != null) {
                returnString=line;
            }
            rd.close();
            return returnString;
        }catch(Exception ex){
            ex.printStackTrace();
        }
        return returnString;
    }
   
    public String sendPost(String url, String auth_string,String params){
        String returnString ="";
        try{
            URL auth = new URL(url);
            HttpsURLConnection connection = (HttpsURLConnection) auth.openConnection();
            connection.setSSLSocketFactory(socket_factory);
            
            //Headers
          connection.setRequestMethod("POST");
          connection.setRequestProperty("Authorization", "Basic "+auth_string);
          connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded"); 
          connection.setDoOutput(true);
            
          OutputStream os = connection.getOutputStream();
          BufferedWriter out = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
          out.write(params);
            
          out.flush();
          out.close();
          os.close();          
          connection.connect();
          
          if (connection.getResponseCode()==200){
                 
                 BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                 String line;
                    while ((line = rd.readLine()) != null) {
                        returnString=line;
                    }
                    rd.close();
                    return returnString;
            } else {
                System.out.print("[Authorization] There was an error with the requesting RPT query, respose code "+connection.getResponseCode());
                throw new Exception();
            }
          }catch(Exception ex){
            ex.printStackTrace();
        }
        return returnString;
    }
    
}
