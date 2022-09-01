<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<html>
			<head>
				<style>
					table {
					font-family: arial, sans-serif;
					border-collapse: collapse;
					width:
					100%;
					}
					td, th {
					border: 1px solid #dddddd;
					text-align: center;
					padding: 8px;
					}
					tr:nth-child(even) {
					background-color: #dddddd;
					}
				</style>
			</head>
			<body>
				<h2><xsl:value-of select='./title[1]'></h2>
				<table>
					<tr>
						<th>Title</th>
						<th>Date</th>
						<th>Link</th>
						<th>Description</th>
					</tr>
					<xsl:for-each select=".//item">
						<tr>
							<td>
								<xsl:value-of select="./title" />
							</td>
							<td>
								<xsl:value-of select="" />
							</td>
							<td>
								<xsl:value-of select="title" />
							</td>
							<td>
								<xsl:value-of select="description" />
							</td>
						</tr>
					</xsl:for-each>
				</table>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>