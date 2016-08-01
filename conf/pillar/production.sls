#!yaml|gpg

environment: production

domain: re-volv.org

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
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  VCdbdpxJ2IHPqp+MBg==
  =j5im
  -----END PGP MESSAGE-----
ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  iI01vR4AmguWKg==
  =mgQl
  -----END PGP MESSAGE-----


#{% endif %}
