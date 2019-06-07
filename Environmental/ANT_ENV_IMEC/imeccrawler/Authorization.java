/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;


import java.net.*;
import java.io.*;
import javax.net.ssl.*;

/**
 *
 * @author gilman
 */
public class Authorization {
    
    private static Authorization auth_instance = null; 
    private String auth_string; 
    private RPTManager rptman=RPTManager.getInstance();
    private ServerConnection servcon = ServerConnection.getInstance(rptman.certificate);
    
    private Authorization(String auth_string) 
    { 
       this.auth_string = auth_string;  
    } 
  
    
    public static Authorization getInstance(String auth_string) 
    { 
        if (auth_instance == null)
            auth_instance = new Authorization(auth_string); 
        return auth_instance; 
    } 
    
    
    private void initialToken(){
         //Form fields  
         String params="grant_type=urn:ietf:params:oauth:grant-type:uma-ticket&audience=policy-enforcer";
         String initial = servcon.sendPost("https://idlab-iot.tengu.io/auth/realms/idlab-iot/protocol/openid-connect/token", auth_string, params);
         if (initial!=null && initial!=""){
             System.out.print("Initial token:");
             rptman.updateDataFromJson(initial);
         }
    }
    
     
    private void refreshToken(){
      //Form fields  
         String params="grant_type=refresh_token&refresh_token="+rptman.rpt_refresh;
         String refreshed = servcon.sendPost("https://idlab-iot.tengu.io/auth/realms/idlab-iot/protocol/openid-connect/token", auth_string, params);
         if (refreshed!=null && refreshed!=""){
             System.out.print("Refreshed token:");
             rptman.updateDataFromJson(refreshed);
         }
    }
             
    
    //get the token
    public String getToken(){
      Long tm_now = System.currentTimeMillis();
      if(((tm_now-rptman.update)/1000)-rptman.rpt_life<0){
        return rptman.rpt;
      }else if((((tm_now-rptman.update)/1000)-rptman.rpt_refresh_life<0) && (((tm_now-rptman.update)/1000)-rptman.rpt_life>0)){
        refreshToken();
      }else{ 
        initialToken();
      }
      return rptman.rpt;
    }
    
    
    
}