#!yaml|gpg

environment: production

domain: revolvbeta.org

repo:
  url: git@github.com:caktus/revolv.git
  branch: master

# Addtional public environment variables to set for the project
env:
    NEW_RELIC_APP_NAME: re-volv production
    NEW_RELIC_MONITOR_MODE: "true"

# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
#http_auth:
#    "re-volv": |-
#      -----BEGIN PGP MESSAGE-----
#      Version: GnuPG v1
#
#      hQEMA9aTfmR7xthMAQf/UFIc+RjmHlOO6H7bT0MFD+BktB8m7l0QYBNjvSrENYwO
#      VLDEp5bLY60QaxDwEP27g2O8SiL670FRLHPvAHN4j44ddQkMT3DUUDYeWWJ1nFiA
#      Z6m+B5sh4MGOVneEjNOnFFP9rBZYVkjlTbE2YH2i83GR4iTUBa1X6htznxBUv9dT
#      hkDe0u7ZMa1qaPOvdxAUxqGTIYMmOESzRL7fHywh4zriyr0Ybplg/o7AzxXUK99K
#      e72yPzxnfz+w2xpk3KesSbLwoTF5woTS2kjtgQVWbQErOK9ggUCV60RLyXNl7O64
#      ThEjFTPxMvWFjhZHDoOxZXyU2ZEZKJ2QrfW9FWMqZ9JHAayP2hE6/1VtzsjoUK3K
#      DYigbUk9JSgki44oP291MuH5dE4gOoaWNMMR006HYEpYCd7I/pO+jjFp11P088Q5
#      Foo3Py/qT4Y=
#      =aHwb
#      -----END PGP MESSAGE-----

# Private environment variables.
# Must be GPG encrypted.
secrets:
    "DB_PASSWORD": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf9G13NuXlim8Bx3LsS6ydmFV6ioatixkXx0XOedwG7poV8
      Du0+/WGDO0umyD2C7X5pfZmmHWXVLw9gg3qJiJtsExUJkkvBsdUL6vjE87W8IDMb
      ibGvz95IBFDba6jRanymVfNNu27117v0fhKF8YEFHpl55zfg6uIIzM7CXrycfvFJ
      m3LNT8iaR8mCm4soBSHiqAYx0tSOhmbKqF7kjFmk4kugFd1rJHRHjEOt86EkM6vz
      1c4nBOAniG/WU96yOm41EiSQt/rwrzQ2daZSZH6iUYn/WgjIn52wjttuHFC+cY6h
      2OKydgQqodz3TzrAM2bztclSBvh/f9BMe392OjHVt9J7ARF1jva1Oqviq/nRRbf8
      GCwMnKPRNkdWUj40T2GnyQ0qenNkL9KQifR4A1GThCtwTWCfbXxFSn5JdSI8hpi8
      2QnoeQDeGu3JQbD1t6ukTUDwmdk0ZZfd26J+xMeSiiWKGZ6wkEz67Tb41iTSOFHr
      QJOdl4kYRMC1HIl7
      =duZ5
      -----END PGP MESSAGE-----

    "SECRET_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf/ZfjG6x8fdbPdB84x4XkkYRYVVBLG9x/qVwWtKXiQ0Lrr
      kvmm1kkadYdINngwYWvQmMB3IAUTCgyTT7rvvg9Bv/8h20eFWKhvRIh6HZ4yDVu2
      1oHj17el4gVYmKYXI2h0uvvHC7/F0fW6b6eoAGs5+i9a2dHnksGpZA4JlC0f8Oov
      lwOADclknR2L5IOxeax5frHGT1IN2bB/bEK72M4JMTTTVhy+MAmffUoZEgwCJe1l
      fw/qvVBt44TGcUSkj7N0YMqj//7bPnfGQa95ngYwlfhZYioWHFtXuL2MLYtMyr8h
      1eUJ6mnxMTzEn8H8Hy3gFmfE7HnoJ96rMlSrrkRi/tJ7AQq3tb1WA3LNjIk3k9rE
      g3jKUSV+OTMqzrGVa4Qj159QmUW2MDgW6yV+lH6Omd7qp7FG/YyIi3BZfh5+jrgp
      4Sf4BivOJncHafqtxFmpLfufUfqdf/9S0jOvSMgIgjBS8cRRdB5ua3OB4nAM8D5+
      wr+jJZlwxQQW4uQ8
      =rCe3
      -----END PGP MESSAGE-----

    "BROKER_PASSWORD": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf/f4NUZVT3RWOGh4p+3xFJ02xX9FpmZkf3kAveIg1bltiZ
      TeLAW9FJjVvh1I5TLZrrII/rYczckF/EOThhCHwLrp5sMbPy8gnYyiSUrL/Bv5Zq
      AwxPmCBPb04gjEbZNUwKKyWHmx8uKnreb6/rsfHDhxflr7xUk2M2VtEmza/RDjf2
      hJiwMx1TKXd+4C72kPQ+dvyFvPlCFkReE/CLFBZmKalS/yIL1tPPbVzJ2E+0i7Vv
      bYelD+Vve1h28DvOmPAp6XnVHpSViiE++zyJq77x2gXvsja6/3bZn9K194WYZk2I
      TNFUznk3vPSVRdzzGfGcjgMNEDaN2ZvbTUPaozNjidJ7ARrijwcUVKHHEJVypueJ
      QP7JXxYcfnn1TItDNk4MVi263UOZvuDXZY8UiE5C3QSuo/0Db/xsvzzgrv71p+Z0
      8UmlrSgGq2wAXSGoomffEQExn6Dj2bTKIAVKWvtKbStLJi2ZefSIghZVYdv4tpTT
      830oMCwnOkqOEcyz
      =b/1z
      -----END PGP MESSAGE-----

    "NEW_RELIC_LICENSE_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf8CdmomEDvs0aq7jesJRyxsSEwBe+PUgBa/gBfjWS9ZPiR
      yJEuyhn00VUzQMp+mGEwJVfT8jZ55PcO8texLhvQPEnEk3B/h4+hOL8gT8AnCnfT
      moYcqYFcBdnq12iu5j3miCatHDdl7mPWckKIFlHmhAVjFt56eknnQHndBxNqxhxj
      IdudML7Ugrx2iY2DUfAsmDf9tVxoCnCX00yQwY0uOAuMAXLZhs0CRHyrLVNEqnRi
      h+cQzSiQJgA5sKqwMnkkljhaeMU6DskZOg2hKfGUzZjsvqersT04adZ0OSlxzTD5
      pl3AlCYjTU16EYv+9cJ2DBx7rntPRiPF1OrwT1T2bdJjATnFNvA7xvwtuGV/d5gG
      rqJjH8Yr1j/EQpb2LEkIyNYT9uq1a23sUzh+OhjS8fjvwQxfRZxfH0t4SC3aPmgA
      s4QeQFqdD02/LG8vyzd5yHrmYnO50TTKnMuyk8VWv2GgrGsV
      =9z5X
      -----END PGP MESSAGE-----

    "LOG_DESTINATION": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf/XImTyudxieMRl1Qh0viuEtqWfbXZMYY482KHFBHLzKWB
      dFBFideQH5sibM3iqo8+L+fA4tpHEiXFyDiCKNV2u5o93kTwdNE20r2NcQ5zTA0r
      Xqono66vJUyVWbl4NSd608HH9vRSCmDxNM+R7hJ75V/fXRXINJFhIZiDaeNKvr7W
      dm2AbKX/lbsJSLf/KFqHY4KJLFqcClMOL9c6CFOAAxYGgSAYN7YPn5ThIU78vomH
      2uej6eioSpdavHJQvvb7DYph5C1J9M8MOd0dSvLwv/YE5yVwen8LAOQuicplFfWQ
      WKm7Vw9LemvOEXcHJf+XAaSIQDky2filDfaane3cpNJYAb0WQu3/cKfhZO7nZnAs
      82u+YBP9lQPPCT7fYNvyEQin+1rJDsdv9hrKg8arWnQO1FyhjKZuiT0ZU7d8GX1H
      PCzyZp7J10n8oIWeBZputJN4vOMh/Aq8Ew==
      =ZhYg
      -----END PGP MESSAGE-----

    "SOCIAL_AUTH_FACEBOOK_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQgAyxPm+UvTNAtzp7s4bLhijXMRzULgATrHYtnKILdJWJkm
      vLXZzNUZrorDsvnnoV0YC+5Ynj8BqupzwFb/lwuNApseywmhYaJGZkQH+LoLfBge
      ti/B6RGpDgnjeIQRwdv4KEP0Szay4Fz5m6DeqbumdGmQWtC+Cat/9tZoWdcJTve7
      Z3u+rCInYXzoysz5XsVxk+vuoeg84536KgFYj0REUdLPJO8OQzseJ9enkRsGdjlm
      ZTaM4q+0Ht+jEqCJjyp9vpLSu+sJ8aRW3sR3NHVVH5ZCYocmKQigKaTkj6fJOOJN
      wHOjlEmoL4LtdwsG61vSi2zyULYk9NHDBn/NXG+LGdJLAejoHwHpTZjBe1nrnF1L
      /h2XEB7Vl7f1DBsL6cuS7UZPFYE3oks/e32G4iAQniy85evAqFHbeoLyVTmG4HYB
      nTHyFBJb7y2yZvDj
      =2JuF
      -----END PGP MESSAGE-----

    "SOCIAL_AUTH_FACEBOOK_SECRET": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf8COMs+oRmM61Rf0kiC9+B/Afoao7icJu2B+582H+nJsTY
      xMkIN7gWn20nnlZzQWIZLVGUc79Lu36Iko+1ks3Jjj5/JG31sWiG30aNcaRFW214
      h0uldqDg+RGzqCpVpKHUl47q9TBs/Lzi9Swc/XczU68rZc0I9vQHWTc0Q94RkbTb
      4M4+aVdACQjjgd5shyrdX7dpotqRhTrSFthwdBldFXT0mB8IyD91mpKL+cBChwvX
      oi1VnahiRxW3FbE/J5GjA5kgnckF9rIYAE1O0KZWoiBKa43MVzYX+ToFjakowwRv
      nm0WfRV0sw89uHsBjtEOKfK4vSkZY23voXNm22wDvtJbARaBIQjaDuBADHxJXvRv
      nnqmLtgDgryWOu2goTAMwBDWsPCBzaGBzGEd/dPy1PGedbEUc4zjMzxZRbMgLL1v
      sTrOVMTM5b225XaaaKG/80+l/JUXVMkwRfzx7g==
      =hcbB
      -----END PGP MESSAGE-----

    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v2

      hQEMA9aTfmR7xthMAQgAgkVqADiOB5i9FqZUmxVb8sJ+WY0ZKLNjwUGoRFtfbJ9a
      YVC8AdqbsltGa4UpRCyBlWrF0yRYSGGspNi6M7h3p9oG9ARQP1AG/YOztjEig/Ya
      QEdkDw5gcDKzeu5ZxXoqLcpzaV+M1wfkz0sl5zEa4Anlk5SyvMnyK6qy7xRS/P6j
      sQVBFx7H6f5npAQ4XlFhCCkn38OHA2sm77m557fC/Vfz/jBOSRQ00QgBiNat8Ctt
      QcgDWkrXxY/3NRszkZ9KEtk8HxHwlEe9dOuhmYfD5zOHDXEfIMitSZJ3kzTBg4X3
      twpsRrq1GDZBB415K/LtBIhcbDomb1keW5t5loxH8dKEAZlv/XboXSqJQ7OMKIoF
      iiT7Bi1Yn2nnPyy2AY94ZBVze1SUNI+iKJg9YX6pImBLWPPUZI/r0GthdfWosJev
      YHlVC7MlYi+xqbYghbhBplJM9hVtvawo/4a0XWMojrjWsot2Vo8LSRfyEB+BFZZ5
      g9zEeq3kcAH0pzwQ7soAjnyowSzA
      =Wr4k
      -----END PGP MESSAGE-----

    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v2

      hQEMA9aTfmR7xthMAQf/ZwKuQFiVa2mNpRWby3tVhEibo7+Evh4ulwHdJXgoEM70
      fEPQQlu8e9Nx7RpGPBoElC+RmbdcqiD3V1kc2ILc7NBB5Ci3zJny+Dr7wgqID5Uh
      k364/43SuVZsPg1wW3bZh/MxqFEszg3XzvX8YN7H7uizkbn6jVuU2SfCPqNI1+mX
      hoZ7MKZ1M7hb6cjMeJhiJfA15gDnBCD/PgROamDZS54dl9JxsjEsDGNqJIADErE3
      FHGyr5N1a8KjIe/9yPZt2gAGuU47T9T1dARrSU2Dzv1OMNE44mjVfHiV1hP8SWf1
      Gual5FKANWnHF8ZQ6FoFC2R5t3+C+Q+fYD91xlStV9JTAW9THTPrnFfT09kP26do
      /peIis30+euuW8dDs1HfRHwiTntI+1ZysIb94puXzXctQyadHwyuEc6tIBABYgBI
      /9naFeVCvFxlWWjXZbvph35dtXo=
      =kIc2
      -----END PGP MESSAGE-----

    "STRIPE_SECRET_KEY": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQgAoGajf/jECL9UTaQrlP+WSYc5sgZFM/NWaKzJq6bRElWT
      ZnG5Yk7n3nmBB/yIwVu0i6xX4ferPoXFqbeeEUcsczoBPNLGNnxDQNc4UQSstcKu
      6WASMqF5c+xycWrgmOeONO9cVpbt4gZkr3sGm49NAJ5BXunewhJh3Rw6nYElvC6u
      PUfC0QM7n20+gB35sHsggjnktiUW5tx4giiwoqoLGIJJdpkAUtZ7jyEfXirF5nM9
      RihVvt3AJIZ8BrG+6LbeVFWMsuSejCkZ7hQfU6N9qVinEp7VgLIkQf57EE9/XqZo
      LF8+BOHq0NKONfpSU9ptTscpLTQlYpVz1nn6tNGBT9JbAQi8EtS+UUXknkvsHfdz
      SNrbiBAfDMs+hRS75RMurJSMSctK96Cx4abhQ/or0S4SX4ZUnlp+SWV7Jedv31Yx
      L6Nf9XBit4KFfqSBvUmPbMv442C7AfQwmaWUKw==
      =LXhi
      -----END PGP MESSAGE-----

    "STRIPE_PUBLISHABLE": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v1

      hQEMA9aTfmR7xthMAQf+Lqe7JC6a7heBdNgOCpXWzL1Xqcj+G/zqRtXMp59Vflvm
      qrbq2i4kFA9nb7gZbO1WSFEwHpTqc5UuDUMfFsFxhOy/t7oq+7EZ6b4nkxPYppbV
      t6ymGWtKI43c+fKtIvkdqjygMFK8dD9Mhtx+m/B25+ZJJ5aWoFQ83KKoMeFPdjoR
      MbyvEzg6XFYljfLFmDfPo2hqyC83J8QEkyXNwEmLQTeJGlxyBInbIg32c2IvcmsI
      7/u2O+g5UuMQ4etd7Fx4K4prWQXwa2Xodc19jbct3xWqw2ME02E5x+XdmTnANGdj
      af0b0mI1206gZH0C0ymEQk4CkuLipqJSjPiaMJOajtJbAUH6nOGuo5t5luA1atpx
      Z77Pncgb0sE2rJxcAlvj+ScAKRbuCWzLMBz6IYFAZjBvhqZfCNHrD9fc4xEjccM9
      cb7Q6NPQr9D54AdWk9eusGsEMiFH/MqEOK6PGA==
      =jo6C
      -----END PGP MESSAGE-----

# Private deploy key. Must be GPG encrypted.
github_deploy_key: |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    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
    =rJBX
    -----END PGP MESSAGE-----


# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
#{% if 'balancer' in grains['roles'] %}
ssl_key: |-
  -----BEGIN RSA PRIVATE KEY-----
  MIIEowIBAAKCAQEA32ThsV8ou/oaL6EANBiIQV2iVmutMPaqtMKrCuC3Knlb6hns
  D15ZC6CKcfhpa+b9ZJvgvVrpEwY4P8HPSDNSVsK3DYZEn9FqrRnBKrFHn0Jh37Pf
  zpFubgxmUPp4Zgjw0scMSLXIvPLSufy4oU5x5AEjetl7e3Ich4ht0Cn4fTJdK2uY
  E+GsWnLBXf1KogHDFeI85F4iUpqnRaBUNxtB1lf/MK0MpwNnzfXEzp6dXKQAuxfA
  h841zm2vjt68tGpTVEA+bOnl0UPc0YRXzlorIQpiwfQjJPAbC2YaLV+L0KM8jOoG
  ctdwjmDqNWKKeaDEeOqIBZ6RwTbc3LzJ4lSYvQIDAQABAoIBAAYM5mv2ZtUIhhMK
  KkY+79nNXms2yV8NHzx8FUPbKDrXRJ0HjLQx2vmMpJNHphtNC0nhSun1/2ALiBR5
  /FI5SZ6d8XVFULB/bIM5slikqoruslXrukEPAU2ruk2xKveggF1FFNkXS1OKxBhT
  dvCvfjgtq7dVEpoaUhl9oXPE3z0Mxi9a7rk1YUUmPJo9+3rxI4FjPLXJQQYEJwWP
  6V+la27FfukIJG5cnYKjesdtZk4E/WcYP1m65ZD5bn6EgHFxrurYPYZaa+ocuzjZ
  G3svH+54JQm94qpi8+OGBhI661iYLTLyWwk4Q7uSnSEVqhGvLMZ/iToWoPAgl+8w
  xEZwNMECgYEA+p6DrOauhoaiAJrMoukT+TVDqQ3PgDLA+b+fVogcYzzSpY/3Ng+C
  bnax14sj8WnWrBASyJSs1Tt/AbLfPsep8clNXW5J9ZxZEerQTTvST0U7K9C7qP17
  HguWxfP6RGkp4614HZREFX95Mg+i//XFBa7TjzYNU26A5ZRBXWhmE/ECgYEA5DC6
  ntxrLrFqrV4A9OTUDUyJgamQZDZ34zdpIYPm6q/i2qIlHQuZOOhbhQCIaWZtpf+6
  6q8qIdrBwen9C7TGGRDEYpFPRxj9D5z05S0Nif9HIw44kAmDXwD57xXq5Ikluesx
  Ar88QByOfKA5rYL1NPUGIx99MTvYtyJONst+bY0CgYEA3NRd7DUbpVfuWaANHqNH
  wTgo1UZhB3IxTh+F9AZdFShb6Byx1MXXxSP7UpS86BS9XsGO+4Tdwcn6AHIvei8O
  1QjujZwHuU65wSrpvpQunUDAgbwcDyzDllbZ1LVFWZBco8yPYWjqkRLQpMbYdreF
  kptYuQEEvvZIx4JaEkdSYtECgYAsrBV80C3zgCwgMI0DZGDXEarBxY5M8BTcWJau
  RwJH45MHtkKJwyGF8IcqLIaIC9NfcgcHtq8K3aac7c/qIMO/WHb5zPS2OIAiNFoF
  G6LQ5zbn9/q+x/399VT4p1PK1caa9R4tKX8EFhMW9s8T1tVmPqmq6pk5sDum7oJd
  W80uaQKBgFlTsJj6Ok+aK/sqR6oOxGcSfVVv74Jvq0bGvKWOGtZRJgIQERkAzja5
  s86nADpUdsOlqVR9D2fHCixFD9XTbs324uuuvopP/O8hm7HcC/FwJbqkae5qmZBd
  Z3GLvV1Nw48a+Nnt2RHssda1waPbK05B05H9ccmEXbo8KF2QTQo6
  -----END RSA PRIVATE KEY-----
ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  MPheYw==
  =kzUe
  -----END PGP MESSAGE-----


#{% endif %}
