#include <gtest/gtest.h>

#include "../../src/DataTypes/LicenseDetails.h"

TEST(App_LicenseDetailsTest, ConstructorDefault)
{
    App::DataTypes::LicenseDetails ld;
    EXPECT_STREQ("", ld.featureID.c_str());
    EXPECT_FALSE(ld.isLicensed);
    EXPECT_STREQ("", ld.expiryDate.c_str());
}

TEST(App_LicenseDetailsTest, ConstructorGRPC)
{
    {
        robotcontrolapp::LicenseInfoResponse_LicenseDetails grpc;

        App::DataTypes::LicenseDetails ld(grpc);
        EXPECT_STREQ("", ld.featureID.c_str());
        EXPECT_FALSE(ld.isLicensed);
        EXPECT_STREQ("", ld.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse_LicenseDetails grpc;
        grpc.set_feature_id("Foo");
        grpc.set_is_licensed(true);

        App::DataTypes::LicenseDetails ld(grpc);
        EXPECT_STREQ("Foo", ld.featureID.c_str());
        EXPECT_TRUE(ld.isLicensed);
        EXPECT_STREQ("", ld.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse_LicenseDetails grpc;
        grpc.set_feature_id("Foo");
        grpc.set_is_licensed(false);

        App::DataTypes::LicenseDetails ld(grpc);
        EXPECT_STREQ("Foo", ld.featureID.c_str());
        EXPECT_FALSE(ld.isLicensed);
        EXPECT_STREQ("", ld.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse_LicenseDetails grpc;
        grpc.set_feature_id("Bar");
        grpc.set_is_licensed(true);
        grpc.set_expiry_date("2026-03-16T10:39:05");

        App::DataTypes::LicenseDetails ld(grpc);
        EXPECT_STREQ("Bar", ld.featureID.c_str());
        EXPECT_TRUE(ld.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", ld.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse_LicenseDetails grpc;
        grpc.set_feature_id("Bar");
        grpc.set_is_licensed(false);
        grpc.set_expiry_date("2026-03-16T10:39:05");

        App::DataTypes::LicenseDetails ld(grpc);
        EXPECT_STREQ("Bar", ld.featureID.c_str());
        EXPECT_FALSE(ld.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", ld.expiryDate.c_str());
    }
}

TEST(App_LicenseInfoTest, ConstructorDefault)
{
    App::DataTypes::LicenseInfo li;
    EXPECT_EQ(0, li.testDurationRemaining);
    EXPECT_TRUE(li.features.empty());
}

TEST(App_LicenseInfoTest, ConstructorGRPC)
{
    {
        robotcontrolapp::LicenseInfoResponse grpc;
        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(0, li.testDurationRemaining);
        EXPECT_TRUE(li.features.empty());
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(1234, li.testDurationRemaining);
        EXPECT_TRUE(li.features.empty());
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        // error: feature has no ID

        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(1234, li.testDurationRemaining);
        EXPECT_EQ(1, li.features.size());
        EXPECT_STREQ("", li.features.begin()->first.c_str());
        EXPECT_STREQ("", li.features.begin()->second.featureID.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        feature1->set_feature_id("Foo");
        feature1->set_is_licensed(true);
        feature1->set_expiry_date("2026-03-16T10:39:05");

        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(1234, li.testDurationRemaining);
        EXPECT_EQ(1, li.features.size());
        EXPECT_STREQ("Foo", li.features.begin()->first.c_str());
        EXPECT_STREQ("Foo", li.features.begin()->second.featureID.c_str());
        EXPECT_TRUE(li.features.begin()->second.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", li.features.begin()->second.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        feature1->set_feature_id("Foo");
        feature1->set_is_licensed(true);
        feature1->set_expiry_date("2026-03-16T10:39:05");

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature2 = grpc.add_licensed_features();
        feature2->set_feature_id("Baz");
        feature2->set_is_licensed(false);
        feature2->set_expiry_date("2027-03-16T10:39:05");

        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(1234, li.testDurationRemaining);
        EXPECT_EQ(2, li.features.size());

        EXPECT_STREQ("Foo", (++li.features.begin())->first.c_str());
        EXPECT_STREQ("Foo", (++li.features.begin())->second.featureID.c_str());
        EXPECT_TRUE((++li.features.begin())->second.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", (++li.features.begin())->second.expiryDate.c_str());

        EXPECT_STREQ("Baz", li.features.begin()->first.c_str());
        EXPECT_STREQ("Baz", li.features.begin()->second.featureID.c_str());
        EXPECT_FALSE(li.features.begin()->second.isLicensed);
        EXPECT_STREQ("2027-03-16T10:39:05", li.features.begin()->second.expiryDate.c_str());
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        feature1->set_feature_id("Foo");
        feature1->set_is_licensed(true);
        feature1->set_expiry_date("2026-03-16T10:39:05");

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature2 = grpc.add_licensed_features();
        feature2->set_feature_id("Baz");
        feature2->set_is_licensed(false);
        feature2->set_expiry_date("2027-03-16T10:39:05");

        // Error: Feature 3 has same ID as feature 2
        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature3 = grpc.add_licensed_features();
        feature3->set_feature_id("Baz");
        feature3->set_is_licensed(false);
        feature3->set_expiry_date("2027-03-16T10:39:05");

        App::DataTypes::LicenseInfo li(grpc);
        EXPECT_EQ(1234, li.testDurationRemaining);
        EXPECT_EQ(2, li.features.size());

        EXPECT_STREQ("Foo", (++li.features.begin())->first.c_str());
        EXPECT_STREQ("Foo", (++li.features.begin())->second.featureID.c_str());
        EXPECT_TRUE((++li.features.begin())->second.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", (++li.features.begin())->second.expiryDate.c_str());

        EXPECT_STREQ("Baz", li.features.begin()->first.c_str());
        EXPECT_STREQ("Baz", li.features.begin()->second.featureID.c_str());
        EXPECT_FALSE(li.features.begin()->second.isLicensed);
        EXPECT_STREQ("2027-03-16T10:39:05", li.features.begin()->second.expiryDate.c_str());
    }
}

TEST(App_LicenseInfoTest, HasFeature)
{
    {
        App::DataTypes::LicenseInfo li;
        EXPECT_FALSE(li.HasFeature(""));
        EXPECT_FALSE(li.HasFeature("Foo"));
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        feature1->set_feature_id("Foo");
        feature1->set_is_licensed(true);
        feature1->set_expiry_date("2026-03-16T10:39:05");

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature2 = grpc.add_licensed_features();
        feature2->set_feature_id("Baz");
        feature2->set_is_licensed(false);
        feature2->set_expiry_date("2027-03-16T10:39:05");

        App::DataTypes::LicenseInfo li(grpc);
        ASSERT_EQ(2, li.features.size());

        EXPECT_TRUE(li.HasFeature("Foo"));
        EXPECT_TRUE(li.HasFeature("Baz"));
        EXPECT_FALSE(li.HasFeature("Bar"));
        EXPECT_FALSE(li.HasFeature(""));
    }
}

TEST(App_LicenseInfoTest, GetFeature)
{
    {
        App::DataTypes::LicenseInfo li;
        try
        {
            li.GetFeature("");
        }
        catch (std::invalid_argument& ex)
        {}

        try
        {
            li.GetFeature("Foo");
        }
        catch (std::invalid_argument& ex)
        {}
    }

    {
        robotcontrolapp::LicenseInfoResponse grpc;
        grpc.set_test_duration_remaining_seconds(1234);

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature1 = grpc.add_licensed_features();
        feature1->set_feature_id("Foo");
        feature1->set_is_licensed(true);
        feature1->set_expiry_date("2026-03-16T10:39:05");

        robotcontrolapp::LicenseInfoResponse_LicenseDetails* feature2 = grpc.add_licensed_features();
        feature2->set_feature_id("Baz");
        feature2->set_is_licensed(false);
        feature2->set_expiry_date("2027-03-16T10:39:05");

        App::DataTypes::LicenseInfo li(grpc);
        ASSERT_EQ(2, li.features.size());

        App::DataTypes::LicenseDetails ldFoo = li.GetFeature("Foo");
        EXPECT_STREQ("Foo", ldFoo.featureID.c_str());
        EXPECT_TRUE(ldFoo.isLicensed);
        EXPECT_STREQ("2026-03-16T10:39:05", ldFoo.expiryDate.c_str());

        App::DataTypes::LicenseDetails ldBaz = li.GetFeature("Baz");
        EXPECT_STREQ("Baz", ldBaz.featureID.c_str());
        EXPECT_FALSE(ldBaz.isLicensed);
        EXPECT_STREQ("2027-03-16T10:39:05", ldBaz.expiryDate.c_str());

        try
        {
            li.GetFeature("");
        }
        catch (std::invalid_argument& ex)
        {}

        try
        {
            li.GetFeature("Bar");
        }
        catch (std::invalid_argument& ex)
        {}
    }
}
