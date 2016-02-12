#!yaml|gpg

environment: production

# FIXME: Change to match production domain name
domain: revolv-prod.cakt.us

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
      Version: GnuPG v2

      hQEMA9aTfmR7xthMAQgAySHCOeh2kZ4wjv5lJMYirjVIC5HX3vxN4lzmBuybDBho
      DPRsVQ8kcRx/6Ev4cxLpJie6aKla3P/cgRE4ZcuMmlUFfqkQzvn9wteae/wOfLD9
      dkhp1Te0mLyqRPG7sl2xK1XzofWXnC8ewqI99aC4Dwe+sy3QwmCqY7QKQuibBJgE
      iua8pGLgDP196lI40XtnPwEryhvrkDjsWCtyKRwnbbzqQSXvZ+CYzxlvGhLnETE8
      WdexQIpbOa6umR3lQ4t1V3B/F+gsbmUDiN37BBRByOXELijPXcze3bIzd1wJQN3m
      WscOR7Arz7WdGECOQScFrl38jy5MNSeeIeVZ/BewjdJbAR8+yiqyotly4lbtx2FH
      RIwGBKEqUPnP42gY5/J2INzsesmiOVEi0LisaqAaAmarA2rJxf6bZoIbRisYLgVu
      jZmTLInTKDNm3O6E9eKQTz/aqoXqAAkHHqFY4Q==
      =jeIe
      -----END PGP MESSAGE-----

    "STRIPE_PUBLISHABLE": |-
      -----BEGIN PGP MESSAGE-----
      Version: GnuPG v2

      hQEMA9aTfmR7xthMAQf/bcmd5uVqZlxqmf30zWkNnZmHW8boY8/t7iIu6n3sMtnA
      uqdVhpmnqFZCFqy8q/t3+Nwi1NeaJeF8nTnzB9UQ6QIBgwDH4vclG1IaqF+m9fgT
      EvDnalJ+Ry0Vxpq3yuxL5GO/LkjdAps0ZBAweC+2SuyquvSU2cLtVM3p2aEdtIXU
      5YJLtN/Feufj88VetXzE35ZMwFvejX9mxJ7Rbou6nFWlXTsf1rU3SC4fpc++H4sM
      ziP32OsI90RzVCLBo7TjBnU0jGNXGK9KaiQThLjrdjz7OH4FKz61YrlcqfR0XfFk
      BvzX0HRjPBAuf4VuxZ6hM6Kj2cV6lJq9e2OLnZwCrNJbASG54NkEvCLKYMN2H9dX
      JAGrk0u8hC4QepTzrsB8UFYhS1a7JCg2OwbHtF84A/ES596z6o/cXNOjgGZuBZns
      FSAej1cMGGcC4bf16+XUMcC2zDN+nrLwoWU0GA==
      =pHqD
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
  78A=
  =1UKe
  -----END PGP MESSAGE-----
ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =YvBw
  -----END PGP MESSAGE-----
#{% endif %}
