<!-- TORS Sales Order Email Template (NetSuite FreeMarker). Record Type: Transaction. Paste into the template's HTML source. Wide layout: card fills 80% of the window, 10% gray border each side. -->
<#-- Order link: try the customer record first, then the sales order's customer (entity). Each try is wrapped so a missing field never breaks the email. -->
<#assign orderLink = "">
<#attempt><#assign orderLink = (customer.custentity_tors_order_link)!""><#recover></#attempt>
<#if !orderLink?has_content><#attempt><#assign orderLink = (transaction.entity.custentity_tors_order_link)!""><#recover></#attempt></#if>
<div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #f4f6f8;">Your order is in. Check its status any time with your Order Status Update link.</div>
<table style="background-color: #f4f6f8;" role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="padding: 24px 0;" align="center">
<table style="width: 80%; max-width: 80%; background-color: #ffffff; border: 1px solid #dde1e7; font-family: Arial,Helvetica,sans-serif; color: #1b2129;" role="presentation" border="0" width="80%" cellspacing="0" cellpadding="0" align="center"><!-- Header -->
<tbody>
<tr>
<td style="padding: 20px 28px; border-bottom: 3px solid #1f4e79;">
<table role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="middle"><a href="https://www.theoringstore.com"><img style="display: block; border: 0; width: 124px; height: auto;" src="https://www.theoringstore.com/store/includes/templates/bootstrap/images/new_logo.png" alt="The O-Ring Store LLC" width="124" /></a></td>
<td style="font-size: 13px; line-height: 19px; color: #5d6775;" align="right" valign="middle"><a style="color: #1f4e79; font-weight: bold; text-decoration: none;" href="mailto:sales@theoringstore.com">sales@theoringstore.com</a><br />208-413-6377</td>
</tr>
</tbody>
</table>
</td>
</tr>
<!-- Greeting -->
<tr>
<td style="padding: 28px 28px 8px 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 4px 0;">Hi ${(contact.firstName)!"there"},</p>
<p style="margin: 0 0 16px 0;">Thank you for your order. It's in our system and headed to the warehouse to be pulled. Here are the details:</p>
</td>
</tr>
<!-- Order details -->
<tr>
<td style="padding: 0 28px;">
<table style="background-color: #f4f6f8; border-radius: 6px;" role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="padding: 14px 18px; font-size: 14px; line-height: 22px;"><span style="color: #5d6775;">Sales Order:</span> <strong>#${transaction.tranId}</strong><br /><span style="color: #5d6775;">Your PO:</span> <strong>${(transaction.otherRefNum)!"Not provided"}</strong><br /><span style="color: #5d6775;">Shipping:</span> <strong>${(transaction.ordertype)!"Standard"}</strong></td>
</tr>
</tbody>
</table>
</td>
</tr>
<!-- Order status button -->
<#if orderLink?has_content>
<tr>
<td style="padding: 28px 28px 8px 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 8px 0; font-size: 18px; font-weight: bold; color: #1f4e79;">Check on your orders any time</p>
<p style="margin: 0 0 18px 0;">This is your own private link. It shows every open order on your account, live from our system: what's on the shelf and ready to go, what's on order and the date we expect it, and tracking numbers once it ships. It's the same link every time, so go ahead and bookmark it.</p>
<table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center">
<tbody>
<tr>
<td style="border-radius: 6px;" align="center" bgcolor="#1f4e79"><a style="display: inline-block; padding: 14px 34px; font-size: 16px; font-weight: bold; color: #ffffff; text-decoration: none; border-radius: 6px; font-family: Arial,Helvetica,sans-serif;" href="${orderLink}" target="_blank" rel="noopener">Order Status Update</a></td>
</tr>
</tbody>
</table>
<p style="margin: 14px 0 0 0; font-size: 12px; line-height: 18px; color: #5d6775; text-align: center;">Button not working? Copy this link into your browser:<br /><a style="color: #1f4e79; word-break: break-all;" href="${orderLink}">${orderLink}</a></p>
</td>
</tr>
<#else>
<tr>
<td style="padding: 28px 28px 8px 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 8px 0; font-size: 18px; font-weight: bold; color: #1f4e79;">Check on your orders any time</p>
<p style="margin: 0;">Every account gets its own private Order Status Update link that shows your open orders live. Reply to this email and we'll send yours right over.</p>
</td>
</tr>
</#if>
<!-- Changes -->
<tr>
<td style="padding: 24px 28px 0 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 6px 0; font-weight: bold;">Need to change something?</p>
<p style="margin: 0;">Reply to this email or send a note to <a style="color: #1f4e79; font-weight: bold;" href="mailto:sales@theoringstore.com">sales@theoringstore.com</a> right away. Your order is already on its way to the warehouse, so the sooner we hear from you, the easier it is to catch.</p>
</td>
</tr>
<!-- Backorders -->
<tr>
<td style="padding: 24px 28px 0 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 6px 0; font-weight: bold;">If anything is backordered</p>
<p style="margin: 0 0 10px 0;">The expected date shows on your Order Status Update page and changes the moment our supplier or our shop updates it. If that date doesn't work for you, just let us know which of these you'd like:</p>
<table style="font-size: 14px; line-height: 21px;" role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="padding: 0 10px 8px 0; color: #1f4e79; font-weight: bold;" valign="top">1.</td>
<td style="padding: 0 0 8px 0;"><strong>Speed it up.</strong> We can expedite production or shipping to get parts to you faster. Extra freight charges may apply.</td>
</tr>
<tr>
<td style="padding: 0 10px 8px 0; color: #1f4e79; font-weight: bold;" valign="top">2.</td>
<td style="padding: 0 0 8px 0;"><strong>Ship what's ready.</strong> We send what's on the shelf now and the rest when it lands. Additional freight will apply.</td>
</tr>
<tr>
<td style="padding: 0 10px 8px 0; color: #1f4e79; font-weight: bold;" valign="top">3.</td>
<td style="padding: 0 0 8px 0;"><strong>Use an alternative.</strong> Our team can find a compound or size that meets your requirements and is in stock today.</td>
</tr>
</tbody>
</table>
</td>
</tr>
<!-- Shipping -->
<tr>
<td style="padding: 20px 28px 0 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 10px 0; font-weight: bold;">How we ship</p>
<table style="font-size: 14px; line-height: 21px; border-top: 1px solid #dde1e7;" role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top" width="150">Same-day shipping</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">Most in-stock, complete orders placed before 4:00 pm Pacific go out the same day.</td>
</tr>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top">Overnight air</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">Order before 12:00 pm Pacific (3:00 pm Eastern) to ship the same day.</td>
</tr>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top">Freight collect</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">Use your own carrier account on orders of $35 and up.</td>
</tr>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top">International</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">Freight collect or FedEx International Priority Overnight. Tariffs, customs and taxes are not included.</td>
</tr>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top">Online orders</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">$10 minimum, shipping from $9.95 at <a style="color: #1f4e79;" href="https://www.theoringstore.com">theoringstore.com</a>. Great for repairs and small jobs.</td>
</tr>
<tr>
<td style="padding: 9px 12px 9px 0; border-bottom: 1px solid #dde1e7; color: #5d6775;" valign="top">B2B account orders</td>
<td style="padding: 9px 0; border-bottom: 1px solid #dde1e7;">$35 minimum plus shipping, pulled and checked by our team.</td>
</tr>
</tbody>
</table>
</td>
</tr>
<!-- O-Ring Handbook -->
<tr>
<td style="padding: 28px 28px 0 28px;">
<table style="border: 1px solid #dde1e7; border-radius: 6px;" role="presentation" border="0" width="100%" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="padding: 0;"><a href="https://oringhandbook.com/" target="_blank" rel="noopener"><img style="display: block; border: 0; width: 100%; max-width: 100%; height: auto; border-radius: 6px 6px 0 0;" src="https://oringhandbook.com/images/banner.jpg" alt="O-Rings in four compounds" width="542" /></a></td>
</tr>
<tr>
<td style="padding: 18px 20px 20px 20px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 6px 0; font-size: 18px; font-weight: bold; color: #1f4e79;">The O-Ring Handbook</p>
<p style="margin: 0 0 16px 0;">Picking a compound or double-checking a size? Our free handbook covers materials, sizes, chemical compatibility and installation tips, all in one spot. Bookmark it for the next time a seal question comes up.</p>
<table role="presentation" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td style="border: 2px solid #1f4e79; border-radius: 6px;" align="center"><a style="display: inline-block; padding: 10px 24px; font-size: 15px; font-weight: bold; color: #1f4e79; text-decoration: none; border-radius: 6px; font-family: Arial,Helvetica,sans-serif;" href="https://oringhandbook.com/" target="_blank" rel="noopener">Open the O-Ring Handbook</a></td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
<!-- Closing -->
<tr>
<td style="padding: 24px 28px 28px 28px; font-size: 15px; line-height: 23px;">
<p style="margin: 0 0 14px 0;">Ordering through our website when you can keeps things fast and accurate for everybody. Thanks for trusting us with your O-Ring and seal needs. We make getting O-Rings easy, and we mean it.</p>
<p style="margin: 0;">Best regards,<br /><strong>The O-Ring Store LLC</strong></p>
</td>
</tr>
<!-- Footer -->
<tr>
<td style="padding: 16px 28px; background-color: #1f4e79; color: #ffffff; font-size: 12px; line-height: 18px;">The O-Ring Store LLC  |  1847 Wilma Dr, Clarkston, WA 99403<br />208-413-6377  |  <a style="color: #ffffff;" href="mailto:sales@theoringstore.com">sales@theoringstore.com</a>  |  <a style="color: #ffffff;" href="https://www.theoringstore.com">theoringstore.com</a>  |  <a style="color: #ffffff;" href="https://oringhandbook.com/">O-Ring Handbook</a><br />ISO 9001:2015 Certified  |  We make getting O-Rings easy!</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
