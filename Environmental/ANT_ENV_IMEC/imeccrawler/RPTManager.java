/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

import java.util.Properties;
import java.io.*;
import com.google.gson.*;

/**
 *
 * @author gilman
 */
public class RPTManager {
    private static RPTManager RPT_instance = null; 
    private String file_path = System.getProperty("user.dir")+"/rpt.properties";
    
    public String rpt="";
    public String rpt_refresh="";
    public int rpt_life=1800;
    public int rpt_refresh_life = 1800;
    public Long update; //in milliseconds
    public Long data_last_update; //in milliseconds
    public String trust_store_path;
    public boolean kafka_use;
    public String output_format;
    public String certificate;
    public String data_folders_path;
    
    private Properties prop = new Properties();
    
    private RPTManager() {
        InputStream input = null;
        try {
		input = new FileInputStream(file_path);
		prop.load(input);
		// get the values 
                rpt=prop.getProperty("rpt");
		rpt_refresh=prop.getProperty("rpt_refresh");
                rpt_life=Integer.parseInt(prop.getProperty("rpt_life"));
                rpt_refresh_life=Integer.parseInt(prop.getProperty("rpt_refresh_life"));
                update=Long.parseLong(prop.getProperty("update"));
                data_last_update=Long.parseLong(prop.getProperty("data_last_update"));
                trust_store_path=prop.getProperty("trust_store_path").replace("\\:", ":");
                output_format=prop.getProperty("output_format");
                kafka_use=Boolean.parseBoolean(prop.getProperty("kafka_use"));
                certificate=prop.getProperty("certificate");
                data_folders_path=prop.getProperty("data_folders_path").replace("\\:", ":");;
	} catch (IOException ex) {
		ex.printStackTrace();
	} finally {
		if (input != null) {
			try {
				input.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
    }
    
    public static RPTManager getInstance() 
    { 
        if (RPT_instance == null) 
            RPT_instance = new RPTManager(); 
        return RPT_instance; 
    } 
    
    
    /**
     * {
    "upgraded": false,
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiA...",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSl...",
    "token_type": "Bearer",
    "not-before-policy": 0
     }
     * @param data
     * @return 
     */
    public int updateDataFromJson(String data){
        Gson gson = new Gson();
        AuthResponse ar = gson.fromJson(data, AuthResponse.class);
        return updateData(ar.access_token, ar.expires_in, ar.refresh_token, ar.refresh_expires_in);
    }
    
    public int setDataLastUpdate(long till_current_time){
        FileOutputStream output = null;
        try{
            output = new FileOutputStream(file_path);
            prop.setProperty("data_last_update",String.valueOf(till_current_time+1));
            prop.store(output, null);
            data_last_update = till_current_time+1;
            output.close();
            return 1;
            
        }catch (IOException io) {
		io.printStackTrace();
                if (output != null) {
			try {
				output.close();
                                return 0;
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
                
	} finally {
		if (output != null) {
			try {
				output.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
        }
    return 0;
    }
    
    public int updateData(String new_rpt, int rpt_exp, String new_rpt_refresh, int refr_exp){
      FileOutputStream output = null;
        try{
            output = new FileOutputStream(file_path);
            
            prop.setProperty("rpt",new_rpt);
	    prop.setProperty("rpt_refresh", new_rpt_refresh);
            prop.setProperty("rpt_life", String.valueOf(rpt_exp));
            prop.setProperty("rpt_refresh_life", String.valueOf(refr_exp));
            Long curr = System.currentTimeMillis();
            prop.setProperty("update",String.valueOf(curr));
            prop.store(output, null);
            rpt=new_rpt;
            rpt_refresh=new_rpt_refresh;
            rpt_life=rpt_exp;
            rpt_refresh_life = refr_exp;
            update = curr;
            output.close();
            return 1;
            
        }catch (IOException io) {
		io.printStackTrace();
                if (output != null) {
			try {
				output.close();
                                return 0;
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
                
	} finally {
		if (output != null) {
			try {
				output.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
        }
    return 0;
    }
    
}
