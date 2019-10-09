#!/bin/bash
echo Deleting All Files in Output
rm -rf ../output/*
echo Obtaining Bluebook Alternatives
python obtain_bluebook_alternatives.py
echo Applying Keyword Classifier
python apply_keyword_classifier.py
echo Generating Manual Treatment Validation File
python generate_manual_classifier_treatment_validation_file.py
echo Generating Online Bluebook File
python generate_bluebook_manual_input_online.py
echo Obtaining Statement Outcomes
python obtain_statement_outcomes.py
echo Deriving Federal Funds Future Data
python derive_federalfundsfuture_data.py
echo Producing Daily Policy Data
python produce_daily_policy_data.py
echo Condensing News Data
python produce_master_news.py

echo Generating Meeting Derived File
python produce_meeting_derived_file.py
