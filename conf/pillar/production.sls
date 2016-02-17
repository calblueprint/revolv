#!yaml|gpg

environment: production

domain: solarseedfund.org

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
  A6VNrOfGgistqv7Qwhm1qV85xQcUtFuYZvsJ9A==
  =hD7p
  -----END PGP MESSAGE-----
ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  Upb+bvH5Im5ulY64ZILDIa4krnnPw8XaYAQ=
  =nY9F
  -----END PGP MESSAGE-----

#{% endif %}
