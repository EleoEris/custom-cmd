@echo off
IF "%1" == "" (
  goto help
) ELSE (
  IF "%1" == "/?" (
    goto help
  ) ELSE (
    IF "%1" == "-h" (
      goto help
    ) ELSE (
      IF "%1" == "--help" (
        goto help
      ) ELSE (
        python "%USERPROFILE%/Desktop/Small Projects/custom cmd/scripts/%1.py" %*
        goto end
      )
    )
  )
)

:help
  echo Hello! Type the name of a script.
  echo.
  echo Available scripts:
  for %%f in ("%~dp0scripts\*.*") do (
    echo - %%~nf
  )

:end
  echo.
