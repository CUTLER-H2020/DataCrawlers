/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Code is adapted from 
 * https://jcalcote.wordpress.com/2010/06/22/managing-a-dynamic-java-trust-store/
 * https://nakov.com/blog/2009/07/16/disable-certificate-validation-in-java-ssl-connections/
 */
package imeccrawler;
import javax.net.ssl.*;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;

import java.security.cert.X509Certificate;

import java.security.KeyStore;
import java.util.List;
import java.util.UUID;
import java.util.ArrayList;
import java.io.*;
/**
 *
 * @author gilman
 */
class ReloadableX509TrustManager implements X509TrustManager {
  private RPTManager rptman=RPTManager.getInstance();
  private String trustStorePath="";
  private X509TrustManager trustManager;
  private List<Certificate> tempCertList=new ArrayList<Certificate>();
  private boolean permanent;

  public ReloadableX509TrustManager(boolean permanent) throws Exception {
    this.permanent = permanent;
    this.trustStorePath = rptman.trust_store_path;
    reloadTrustManager();
  }

  @Override
  public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {
    trustManager.checkClientTrusted(chain, authType);
  }

  @Override
  public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
    try {
      trustManager.checkServerTrusted(chain, authType);
    } catch (CertificateException cx) {
        System.out.println("The certificate error. Would you like to ignore it this time? (y/n)");
        addServerCertAndReload(chain[0], permanent);
        trustManager.checkServerTrusted(chain, authType);
    }
  }

  @Override
  public X509Certificate[] getAcceptedIssuers() {
    X509Certificate[] issuers = trustManager.getAcceptedIssuers();
    return issuers;
  }

  private void reloadTrustManager() throws Exception {
    // load keystore from specified cert store (or default)
    KeyStore ts = KeyStore.getInstance(KeyStore.getDefaultType());
    InputStream in = new FileInputStream(trustStorePath);
    try { ts.load(in, null); }
    finally { in.close(); }

    // add all temporary certs to KeyStore (ts)
    for (Certificate cert : tempCertList) {
      ts.setCertificateEntry(UUID.randomUUID().toString(), cert);
    }

    // initialize a new TMF with the ts we just loaded
    TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
    tmf.init(ts);

    // acquire X509 trust manager from factory
    TrustManager tms[] = tmf.getTrustManagers();
    for (int i = 0; i < tms.length; i++) {
      if (tms[i] instanceof X509TrustManager) {
        trustManager = (X509TrustManager)tms[i];
        return;
      }
    }

    throw new Exception("No X509TrustManager in TrustManagerFactory");
  }

  private void addServerCertAndReload(Certificate cert, boolean permanent) {
    try {
      if (permanent) {
        //to be implemented
        // import the cert into file trust store
        // Google "java keytool source" or just ...
        //Runtime.getRuntime().exec("keytool -importcert ...");
      } else {
        tempCertList.add(cert);
      }
      reloadTrustManager();
    } catch (Exception ex) { 
        ex.printStackTrace(); 
    }
  }
}