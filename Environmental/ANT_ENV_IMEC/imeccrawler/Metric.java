/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

/**
 *
 * @author gilman
 */
public class Metric {
    public String id;
    public String description;
    public Object annotations;
    public String granularity;
    public String type;
    
    public String printInformation(){
        return "{\"id\":\""+id+"\",\"description\":\""+description+"\",\"annotations\":"+annotations.toString()+",\"granularity\":\""+granularity+"\",\"type\":\""+type+"\"}";
    }
    
}
