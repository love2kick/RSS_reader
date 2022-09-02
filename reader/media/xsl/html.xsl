<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/content">
		<html>
			<head>
				<style>
					table {
					font-family: arial, sans-serif;
					border-collapse: collapse;
					width: 100%;
					}

					td,
					th {
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
				<h2>
					<xsl:value-of select='./feed'/>
				</h2>
				<xsl:for-each select="./items/*">
					<table>
						<tr>
							<th>
								<p class='article'><xsl:value-of select="./TITLE" /></p>
							</th>
						</tr>
						<tr>
							<td>
								<p class='date'><xsl:value-of select="./DATE" /></p>
							</td>
						</tr>
						<tr>
							<td>
								<a class='link'>
									<xsl:attribute name='href'>
										<xsl:value-of select="./LINK" />
									</xsl:attribute>
									<xsl:value-of select="./LINK" />
								</a>
							</td>
						</tr>
						<tr>
							<td>
								<p class='description'><xsl:value-of select="./DESCRIPTION" /></p>
							</td>
						</tr>
					</table>
				</xsl:for-each>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>