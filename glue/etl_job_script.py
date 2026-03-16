import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1773643365781 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["SOURCE_PATH"], "recurse": True}, transformation_ctx="AmazonS3_node1773643365781")

# Script generated for node Aggregate
Aggregate_node1773643370641 = sparkAggregate(glueContext, parentFrame = AmazonS3_node1773643365781, groups = ["country"], aggs = [["amount", "sum"]], transformation_ctx = "Aggregate_node1773643370641")

# Script generated for node Rename Field
RenameField_node1773643375107 = RenameField.apply(frame=Aggregate_node1773643370641, old_name="`sum(amount)`", new_name="total_mount", transformation_ctx="RenameField_node1773643375107")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=RenameField_node1773643375107, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1773642966405", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1773643382471 = glueContext.getSink(path="TARGET_PATH", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["country"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1773643382471")
AmazonS3_node1773643382471.setCatalogInfo(catalogDatabase="default",catalogTableName="sales_quality_check")
AmazonS3_node1773643382471.setFormat("glueparquet", compression="snappy")
AmazonS3_node1773643382471.writeFrame(RenameField_node1773643375107)
job.commit()
