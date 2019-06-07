/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;

import java.util.ArrayList;
import java.util.HashMap;

/**
 *
 * @author gilman
 */
public class MetricValue {
    public ArrayList<String> columns;
    public ArrayList<ArrayList<String>> values;
    
    public ArrayList<Value> getValues(){
        ArrayList value_objects = new ArrayList();
        if(values!=null){
            for(int i=0;i<values.size();i++){
                ArrayList<String> ar = (ArrayList) values.get(i);
                Value v = new Value(Long.parseLong(ar.get(0)),ar.get(1),ar.get(2),Float.parseFloat(ar.get(3)));
                value_objects.add(v);
            }
        }
        return value_objects;
    }
    
    public HashMap getValuesGroupedBySourceID(ArrayList<Value> value_objects){
       HashMap result = new HashMap();
       for(int i=0;i<value_objects.size();i++){
           Value val = value_objects.get(i);
           if(result.containsKey(val.sourceId)){
               ArrayList vals = (ArrayList)result.get(val.sourceId);
               vals.add(val);
               result.put(val.sourceId,vals);
           }else{
               ArrayList<Value> ar = new ArrayList();
               ar.add(val);
               result.put(val.sourceId,ar);
           }
       }
       return result;
    }
    
    
}
