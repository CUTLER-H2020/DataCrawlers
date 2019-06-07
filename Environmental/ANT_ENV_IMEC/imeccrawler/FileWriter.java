/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;
import java.util.ArrayList;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.File;


/**
 *
 * @author gilman
 */
public class FileWriter {
    
    private String output_format;
    private String extension;
    
    public FileWriter(String output_format){
        this.output_format=output_format;
        if(output_format.equalsIgnoreCase("CSV")){
            extension = ".csv";
        }else if (output_format.equalsIgnoreCase("JSON")){
            extension = ".json";
        } else{
           extension = ".txt";
        }
        
    }
    
    public boolean writeToFile(String metric, String sourceId, ArrayList<Value> values, String folder_path){
    
       BufferedWriter writer = null;
    try {
        File file = new File(folder_path+"/"+metric+"/"+sourceId+"_"+System.currentTimeMillis()+extension);   
        file.getParentFile().mkdirs();
        writer = new BufferedWriter(new OutputStreamWriter(
            new FileOutputStream(file), "utf-8"));      
          for(int i=0;i<values.size();i++){
            writer.write(values.get(i).toString(output_format));
            writer.newLine();
          }
        } catch (IOException ex) {
            // Report
        } finally {
            try {writer.close();} catch (Exception ex) {/*Report*/}

    }
        
        return true;
    }
    
}
