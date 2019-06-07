/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package imeccrawler;
import com.google.gson.annotations.SerializedName;

/**
 *
 * @author gilman
 */
public class AuthResponse {
    
  public String upgraded;
  public String access_token;
  public int expires_in;
  public int refresh_expires_in;
  public String refresh_token;
  public String token_type;
  @SerializedName("not-before-policy")
  public int not_before_policy ;
}
