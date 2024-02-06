import pandas as pd
from sklearn.linear_model import LogisticRegression
from causalml.match import NearestNeighborMatch

subset_beforeT = pd.read_csv("subset_beforeT.csv")
subset_afterT_member = pd.read_csv("subset_afterT_member.csv")
subset_afterT_nonmember = pd.read_csv("subset_afterT_nonmember.csv")
subset_beforeT = subset_beforeT.head(5000)
subset_afterT_member = subset_afterT_member.head(200)
subset_afterT_nonmember = subset_afterT_nonmember.head(5000)

subset_afterT_lr = pd.concat([subset_afterT_nonmember, subset_afterT_member], ignore_index=True)
subset_afterT_lr = subset_afterT_lr.drop(columns=["Rev", "Date"])
subset_beforeT_prop = subset_beforeT.drop(columns=["Rev", "Date"])
subset_afterT_member_prop = subset_afterT_member.drop(columns=["Rev", "Date"])
subset_afterT_nonmember_prop = subset_afterT_nonmember.drop(columns=["Rev", "Date"])

logistic_model = LogisticRegression()
logistic_model.fit(subset_afterT_lr.drop("Y", axis=1), subset_afterT_lr["Y"])

subset_beforeT['Propensity_Score'] = logistic_model.predict_proba(subset_beforeT_prop.drop("Y", axis=1))[:, 1]
subset_afterT_member['Propensity_Score'] = logistic_model.predict_proba(subset_afterT_member_prop.drop("Y", axis=1))[:, 1]
subset_afterT_nonmember['Propensity_Score'] = logistic_model.predict_proba(subset_afterT_nonmember_prop.drop("Y", axis=1))[:, 1]

subset_beforeT_matching = pd.concat([subset_beforeT, subset_afterT_member], ignore_index=True).drop(columns=["Rev", "Date"])
subset_afterT_matching = pd.concat([subset_afterT_member, subset_afterT_nonmember], ignore_index=True).drop(columns=["Rev", "Date"])

del logistic_model
del subset_beforeT_prop
del subset_afterT_member_prop
del subset_afterT_nonmember_prop
del subset_afterT_lr

matcher = NearestNeighborMatch(caliper=0.2, replace=False)
matched_data_after = matcher.match(data=subset_afterT_matching, treatment_col="Y", score_cols=['Propensity_Score'])
# subset_afterT_nonmember['Matched'] = False
# subset_afterT_nonmember.loc[matched_data_after.index, 'Matched'] = True

# matched_counts = subset_afterT_nonmember['Matched'].value_counts()

matched_data_before = matcher.match(data=subset_beforeT_matching, treatment_col="Y", score_cols=['Propensity_Score'])
# subset_beforeT['Matched'] = False
# subset_beforeT.loc[matched_data_before.index, 'Matched'] = True
del matcher
del subset_beforeT_matching
del subset_afterT_matching

# matched_nonloyalty_beforeT = matched_data_before[matched_data_before['Y'] == 0]
# matched_nonloyalty_afterT = matched_data_after[matched_data_after['Y'] == 0]

# avg_revenue_nonloyalty_beforeT = matched_nonloyalty_beforeT["Rev"].mean()
# avg_revenue_nonloyalty_afterT = matched_nonloyalty_afterT["Rev"].mean()
# avg_revenue_loyalty = subset_afterT_member["Rev"].mean()


# matched_nonloyalty_beforeT = matched_nonloyalty_beforeT.drop(columns=["Receipt", "Rev", "Date", "Time", "Y"])
# matched_nonloyalty_afterT = matched_nonloyalty_afterT.drop(columns=["Receipt", "Rev", "Date", "Time", "Y"])

# for col in matched_nonloyalty_beforeT.columns: 
#     mean_nlb = matched_nonloyalty_beforeT[col].mean()
#     sd_nlb = matched_nonloyalty_beforeT[col].std()
#     mean_nla = matched_nonloyalty_afterT[col].mean()
#     sd_nla = matched_nonloyalty_afterT[col].std()
#     mean_lm = loyalty_members[col].mean()
    
#     fraction_before = (mean_nlb - mean_lm) / sd_nlb
#     fraction_after = (mean_nla - mean_lm) / sd_nla
    
#     print()
#     print(col)
#     print(f"BEFORE T & LOYMEM: {fraction_before}")
#     print(f"AFTER T & LOYMEM: {fraction_after}")
#     print()
    
    
# test = loyalty_members["Propensity_Score"][1:10]
# plt.scatter(, [0] *loyalty_members["Propensity_Score"].shape()) 
    

